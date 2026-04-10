"""Anwendungskern für Benutzerdaten."""
from collections.abc import Mapping
from dataclasses import asdict
from typing import Any, Final

from fastapi import Request
from jwcrypto.common import JWException
from keycloak import KeycloakAuthenticationError, KeycloakOpenID
from loguru import logger

from mitarbeiter.config import keycloak_config
from mitarbeiter.security.exceptions import AuthorizationError, LoginError
from mitarbeiter.security.role import Role
from mitarbeiter.security.user import User

__all__ = ["TokenService"]


class TokenService:
    """Tokenmanagement von Keycloak."""

    def __init__(self) -> None:
        """Initialisierung."""
        self.keycloak = KeycloakOpenID(**asdict(keycloak_config))

    def token(self, username: str | None, password: str | None) -> Mapping[str, str]:
        """Access und Refresh Token des Users werden ermittelt."""
        if username is None or password is None:
            raise LoginError(username=username)

        logger.debug("username={}, password={}", username, password)
        try:
            token = self.keycloak.token(username, password)
        except KeycloakAuthenticationError as err:
            logger.debug("err={}", err)
            raise LoginError(username=username) from err

        logger.debug("token={}", token)
        return token

    def _get_token_from_request(self, request: Request) -> str:
        """Token aus "Authorization"-String extrahieren."""
        authorization_header: Final = request.headers.get("Authorization")
        logger.debug("authorization_header={}", authorization_header)
        if authorization_header is None:
            raise AuthorizationError
        try:
            authorization_scheme, bearer_token = authorization_header.split()
        except ValueError as err:
            raise AuthorizationError from err
        if authorization_scheme.lower() != "bearer":
            raise AuthorizationError
        return bearer_token

    def get_user_from_token(self, token: str) -> User:
        """Userdaten aus cod. Token extrahieren."""
        try:
            token_decoded: Final = self.keycloak.decode_token(token=token)
        except (JWException) as err:
            raise AuthorizationError from err

        logger.debug("token_decoded={}", token_decoded)
        username: Final[str] = token_decoded["preferred_username"]
        email: Final[str] = token_decoded["email"]
        nachname: Final[str] = token_decoded["name"]
        vorname: Final[str] = token_decoded["given_name"]
        roles = self.get_roles_from_token(token_decoded)

        user: Final = User(
            username=username,
            email=email,
            nachname=nachname,
            vorname=vorname,
            roles=roles
        )
        logger.debug("user={}", user)
        return user

    def get_user_from_request(self, request: Request) -> User:
        """Userdaten aus cod. "Authorization"-String extrahieren."""
        bearer_token: Final = self._get_token_from_request(request)
        user: Final = self.get_user_from_token(token=bearer_token)
        logger.debug("user={}", user)
        return user

    def get_roles_from_token(self, token: str | Mapping[str, Any]) -> list[Role]:
        """Rollen aus Access Token extrahieren."""
        if isinstance(token, str):
            token_decoded = self.keycloak.decode_token(token=token)
        else:
            token_decoded = token
        logger.debug("token_decoded={}", token_decoded)

        roles: Final[str] = token_decoded["ressource_access"][self.keycloak.client_id][
            "roles"
        ]
        roles_enum: Final = [Role[role.upper()] for role in roles]
        logger.debug("roles_enum={}", roles_enum)
        return roles_enum
