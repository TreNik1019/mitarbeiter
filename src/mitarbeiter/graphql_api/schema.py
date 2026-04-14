"""Schema für GraphQL."""

from collections.abc import Sequence
from typing import Final

import strawberry
from fastapi import Request
from loguru import logger
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info

from mitarbeiter.config.graphql import graphql_ide
from mitarbeiter.graphql_api.graphql_types import (
    CreatePayload,
    LoginResult,
    MitarbeiterInput,
    Suchparameter,
)
from mitarbeiter.repository import MitarbeiterRepository, Pageable
from mitarbeiter.router.mitarbeiter_model import MitarbeiterModel
from mitarbeiter.security import Role, TokenService, UserService
from mitarbeiter.service import (
    MitarbeiterDTO,
    MitarbeiterService,
    MitarbeiterWriteService,
    NotFoundError,
)

__all__ = ["graphql_router"]


_repo: Final = MitarbeiterRepository()
_service: MitarbeiterService = MitarbeiterService(repo=_repo)
_user_service: UserService = UserService()
_write_service: MitarbeiterWriteService = MitarbeiterWriteService(
    repo=_repo,
    user_service=_user_service,
)
_token_service: Final = TokenService()


@strawberry.type
class Query:
    """GraphQL-Query-Objekt."""

    @strawberry.field
    def mitarbeiter(
        self,
        mitarbeiter_id: strawberry.ID,
        info: Info
    ) -> MitarbeiterDTO | None:
        """Mitarbeiter suchen."""
        logger.debug("mitarbeiter_id={}", mitarbeiter_id)

        request: Final[Request] = info.context.get("request")
        current_user: Final = _token_service.get_user_from_request(request=request)
        if current_user is None:
            return None

        try:
            mitarbeiter_dto: Final = _service.find_by_id(
                mitarbeiter_id=int(mitarbeiter_id),
                current_user=current_user
            )
        except NotFoundError:
            return None
        logger.debug("{}", mitarbeiter_dto)
        return mitarbeiter_dto

    @strawberry.field
    def mmitarbeiter(
        self,
        suchparameter: Suchparameter,
        info: Info
    ) -> Sequence[MitarbeiterDTO]:
        """Mitarbeiter anhand von Suchparametern suchen."""
        logger.debug("suchparameter={}", suchparameter)

        request: Final[Request] = info.context["request"]
        current_user: Final = _token_service.get_user_from_request(request)
        if current_user is None or Role.ADMIN not in current_user.roles:
            return []

        suchparameter_dict: Final[dict[str, str]] = dict(vars(suchparameter))
        suchparameter_filtered = {
            key: value
            for key, value in suchparameter_dict.items()
            if value is not None and value
        }
        logger.debug("suchparameter_filtered={}", suchparameter_filtered)

        pageable: Final = Pageable.create(size=str(0))
        try:
            mitarbeiter_dto: Final = _service.find(
                suchparameter=suchparameter_filtered,
                pageable=pageable
            )
        except NotFoundError:
            return []
        logger.debug("{}", mitarbeiter_dto)
        return mitarbeiter_dto.content


@strawberry.type
class Mutation:
    """Mutationen, um Mitarbeiterdaten anzulegen, zu ändern oder zu löschen."""

    @strawberry.mutation
    def create(
        self,
        mitarbeiter_input: MitarbeiterInput
    ) -> CreatePayload:
        """Einen neuen Mitarbeiter anlegen."""
        logger.debug("mitarbeiter_input={}", mitarbeiter_input)

        mitarbeiter_dict = mitarbeiter_input.__dict__
        mitarbeiter_dict["werksausweis"] = mitarbeiter_input.werksausweis.__dict__
        mitarbeiter_dict["Auftraege"] = [
            auftrag.__dict__ for auftrag in mitarbeiter_input.auftraege
        ]

        mitarbeiter_model: Final = MitarbeiterModel.model_validate(mitarbeiter_dict)

        mitarbeiter_dto: Final = _write_service.create(
            mitarbeiter=mitarbeiter_model.to_mitarbeiter()
        )
        payload: Final = CreatePayload(id=mitarbeiter_dto.id)

        logger.debug("{}", payload)
        return payload


@strawberry.mutation
def login(self, username: str, password: str) -> LoginResult:   # noqa: ARG001
    """Token zu Benutzername und Passwort ermitteln."""
    logger.debug("username={}, password={}", username, password)
    token_mapping = _token_service.token(
        username=username,
        password=password
    )

    token = token_mapping["access_token"]
    current_user = _token_service.get_user_from_token(token)
    roles: Final = [role.value for role in current_user.roles]
    return LoginResult(token=token, expiresIn="1d", roles=roles)


schema: Final = strawberry.Schema(query=Query, mutation=Mutation)


Context = dict[str, Request]


def get_context(request: Request) -> Context:
    """Context-Funktion, um Request-Objekt in GraphQL-Resolvern verfügbar zu machen."""
    return {"request": request}


graphql_router: Final = GraphQLRouter[Context](
    schema=schema,
    get_context=get_context,
    graphql_ide=graphql_ide
)
