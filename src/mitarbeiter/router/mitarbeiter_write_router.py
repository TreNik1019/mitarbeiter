"""MitarbeiterWriteRouter."""

from typing import Annotated, Final

from fastapi import APIRouter, Depends, Request, Response, status
from loguru import logger

from mitarbeiter.problem_details import create_problem_details
from mitarbeiter.router.constants import IF_MATCH, IF_MATCH_MIN_LEN
from mitarbeiter.router.dependencies import get_write_service
from mitarbeiter.router.mitarbeiter_model import MitarbeiterModel
from mitarbeiter.router.mitarbeiter_update_model import MitarbeiterUpdateModel
from mitarbeiter.security import Role, RolesRequired
from mitarbeiter.service import MitarbeiterWriteService

__all__ = ["mitarbeiter_write_router"]


mitarbeiter_write_router: Final = APIRouter(tags=["Schreiben"])


@mitarbeiter_write_router.post("")
def post(
    mitarbeiter_model: MitarbeiterModel,
    request: Request,
    service: Annotated[MitarbeiterWriteService, Depends(get_write_service)],
) -> Response:
    """POST-Request, um einen neuen Mitarbeiter anzulegen.

    :param mitarbeiter_model: Mitarbeiterdaten als Pydantic-Model
    :param request: Injiziertes Request-Objekt von FastAPI bzw. Starlette
                    mit der Request-URL
    :param service: Injizierter Service für Geschäftslogik
    :rtype: Response
    :raises ValidationError: Falls es bei Pydantic Validierungsfehler gibt
    :raises EmailExistsError: Falls die Emailadresse bereits existiert
    :raises UsernameExistsError: Falls der Benutzername bereits existiert
    """
    logger.debug("mitarbeiter_model={}", mitarbeiter_model)
    mitarbeiter_dto: Final = service.create(
        mitarbeiter=mitarbeiter_model.to_mitarbeiter()
    )
    logger.debug("mitarbeiter_dto={}", mitarbeiter_dto)

    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={"Location": f"{request.url}/{mitarbeiter_dto.id}"},
    )


@mitarbeiter_write_router.put(
    "/{mitarbeiter_id}",
    dependencies=[Depends(RolesRequired([Role.ADMIN, Role.MITARBEITER]))],
)
def put(
    mitarbeiter_id: int,
    mitarbeiter_update_model: MitarbeiterUpdateModel,
    request: Request,
    service: Annotated[MitarbeiterWriteService, Depends(get_write_service)],
) -> Response:
    """PUT-Request, aktualisieren.

    :param mitarbeiter_id: ID des zu aktualisierenden Mitarbeiters als Pfadparameter
    :param request: Injiziertes Request-Objekt von FastAPI bzw. Starlette
                    mit If-Match im Header
    :param service: Injizierter Service für Geschäftslogik
    :return: Response mit Statuscode 204
    :rtype: Response
    :raises ValidationError: Falls es bei Marshmallow Validierungsfehler gibt
    :raises EmailExistsError: Falls die neue Emailadresse bereits
    :raises NotFoundError: Falls zur id kein Mitarbeiter existiert
    :raises VersionOutdatedError: Falls die Versionsnummer nicht aktuell ist
    """
    if_match_value: Final = request.headers.get(IF_MATCH)
    logger.debug(
        "mitarbeiter_id={}, if_match={}, mitarbeiter_update_model={}",
        mitarbeiter_id,
        if_match_value,
        mitarbeiter_update_model,
    )

    if if_match_value is None:
        return create_problem_details(
            status_code=status.HTTP_428_PRECONDITION_REQUIRED,
        )

    if (
        len(if_match_value) < IF_MATCH_MIN_LEN
        or not if_match_value.startswith('"')
        or not if_match_value.endswith('"')
    ):
        return create_problem_details(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
        )

    version: Final = if_match_value[1:-1]
    try:
        version_int: Final = int(version)
    except ValueError:
        return Response(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
        )

    mitarbeiter: Final = mitarbeiter_update_model.to_mitarbeiter()
    mitarbeiter_modified: Final = service.update(
        mitarbeiter=mitarbeiter,
        mitarbeiter_id=mitarbeiter_id,
        version=version_int,
    )
    logger.debug("mitarbeiter_modified={}", mitarbeiter_modified)

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
        headers={"ETag": f'"{mitarbeiter_modified.version}"'},
    )


@mitarbeiter_write_router.delete(
    "/{mitarbeiter_id}",
    dependencies=[Depends(RolesRequired([Role.ADMIN, Role.MITARBEITER]))],
)
def delete_by_id(
    mitarbeiter_id: int,
    service: Annotated[MitarbeiterWriteService, Depends(get_write_service)],
) -> Response:
    """DELETE-Request, um einen Mitarbeiter anhand seiner ID zu löschen.

    :param mitarbeiter_id: ID des zu löschenden Mitarbeiters
    :param service: Injizierter Service für Geschäftslogik
    :return: Response mit Statuscode 204
    :rtype: Response
    """
    logger.debug("mitarbeiter_id={}", mitarbeiter_id)
    service.delete_by_id(mitarbeiter_id=mitarbeiter_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
