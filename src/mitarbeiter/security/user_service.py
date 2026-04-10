"""Management der Benutzerdaten mit dem REST-API von Keycloak."""

from dataclasses import asdict
from typing import Any, Final, cast

from keycloak import KeycloakAdmin, KeycloakConnectionError
from loguru import logger
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

from mitarbeiter.config import keycloak_admin_config
from mitarbeiter.security.role import Role
from mitarbeiter.security.user import User

__all__ = ["UserService"]

class UserService:
    """Schnittstelle für das Management der Benutzerdaten von Keycloak."""

    def __init__(self) -> None:
        """Initialisierung."""
        self.keycloak_admin = KeycloakAdmin(**asdict(keycloak_admin_config))

        disable_warnings(InsecureRequestWarning)
        try:
            self.client_uuid: str = cast(
                "str",
                self.keycloak_admin.get_client_id(keycloak_admin_config.client_id),
            )
            logger.debug("client_id={} für 'python-client'", self.client_uuid)
            roles = self.keycloak_admin.get_client_roles(client_id=self.client_uuid)
            roles_mitarbeiter = [role for role in roles if role["name"] == "mitarbeiter"]
            self.rolle_mitarbeiter = roles_mitarbeiter[0]
            logger.debug("rolle_mitarbeiter={}", self.rolle_mitarbeiter)
        except KeycloakConnectionError:
            logger.error("Keine Verbindung zu Keycloak!")
            self.client_uuid = "N/A"
            self.rolle_mitarbeiter = None

    def username_exists(self, username: str) -> bool:
        """Existiert Benutzer bereits?"""
        logger.debug("username={}", username)

        user_id: Final = self.keycloak_admin.get_user_id(username)
        logger.debug("user_id={}", user_id)
        exist: Final = user_id is not None
        logger.debug("exists={}", exists)
        return exists

    def email_exists(self, email: str) -> bool:
        """Existiert Email bereits?"""
        logger.debug("email={}", email)

        users: Final = self.keycloak_admin.get_users(query={"email": email})
        logger.debug("users={}", users)
        exists: Final = len(users) > 0
        logger.debug("exists={}", exists)
        return exists

    def create_user(self, user: User) -> str:
        """Neuen User in Keycloak anlegen."""
        logger.debug("user={}", user)

        user_id: Final = self.keycloak_admin.create_user(
            payload={
                "username": user.username,
                "email": user.email,
                "lastName": user.nachname,
                "firstName": user.vorname,
                "credentials": [{"value": user.password, "type": "password"}],
                "enabled": True,
            },
            exist_ok=False,
        )
        logger.debug("user_id={}", user_id)

        self.keycloak_admin.assign_client_role(
            user_id=user_id, client_id=self.client_uuid, roles=[self.rolle_mitarbeiter]
        )
        return user_id

    def remove_all_users(self) -> None:         #noch anschauen!
        """Alle User außer 'admin' aus Keycloak entfernen."""
        # https://www.keycloak.org/docs-api/latest/rest-api/#_users:
        # GET /admin/realms/{realm}/users
        # keycloak_admin.get_users(query={"username": "foo"})
        kc_users: Final = self.keycloak_admin.get_users()
        for kc_user in kc_users:
            if kc_user.get("username") == "admin":
                continue
            # https://www.keycloak.org/docs-api/latest/rest-api/#_users:
            # DELETE /admin/realms/{realm}/users/{user-id}
            self.keycloak_admin.delete_user(kc_user.get("id"))

    def find_user_by_username(self, username: str) -> User | None:
        """User anhannd Benutzernamen suchen."""

        kc_users: Final = self.keycloak_admin.get_users({"username": username})
        if not kc_users:
            return None
        kc_user: Final = kc_users[0]
        logger.debug("kc_user={}", kc_user)

        kc_roles: Final[Any] = self.keycloak_admin.get_all_roles_of_user(kc_user["id"])
        kc_client_roles = kc_roles["clientMappings"][keycloak_admin_config.client_id][
            "mappings"
        ]
        logger.debug("kc_client_roles={}", kc_client_roles)

        roles: Final = [Role[role["name"].upper()] for role in kc_client_roles]
        user: Final = User(
            username=kc_user["username"],
            email=kc_user["email"],
            nachname=kc_user["lastName"],
            vorname=kc_user["firstName"],
            roles=roles,
        )
        logger.debug("user={}", user)
        return user
