"""MitarbeiterGetRouter."""

from dataclasses import asdict
from typing import Annotated, Any, Final

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import JSONResponse
from loguru import logger

from mitarbeiter.repository import Pageable
from mitarbeiter.repository.slice import Slice
from mitarbeiter.router.constants import ETAG, IF_NONE_MATCH, IF_NONE_MATCH_MIN_LEN
from mitarbeiter.router.dependencies import get_service
from mitarbeiter.router.page import Page
from mitarbeiter.security import Role, RolesRequired, User
from mitarbeiter.service import MitarbeiterDTO, MitarbeiterService

__all__ = ["mitarbeiter_router"]


# APIRouter auf Basis der Klasse Router von Starlette
mitarbeiter_router: Final = APIRouter(tags=["Lesen"])


@mitarbeiter_router.get(
    "/{mitarbeiter_id}",
    dependencies=[Depends(RolesRequired([Role.ADMIN, Role.MITARBEITER]))],
)
def get_by_id(
    mitarbeiter_id: int,
    request: Request,
    service: Annotated[MitarbeiterService, Depends(get_service)],
) -> Response:
    """Suche mit der Mitarbeiter-ID."""
    # User-Objekt ist durch Depends(RolesRequired()) in Request.state gepuffert
    user: Final[User] = request.state.current_user
    logger.debug("mitarbeiter_id={}, user={}", mitarbeiter_id, user)

    mitarbeiter: Final = service.find_by_id(
        mitarbeiter_id=mitarbeiter_id,
        current_user=user
    )
    logger.debug("{}", mitarbeiter)

    if_none_match: Final = request.headers.get(IF_NONE_MATCH)
    if (
        if_none_match is not None
        and len(if_none_match) >= IF_NONE_MATCH_MIN_LEN
        and if_none_match.startswith('"')
        and if_none_match.endswith('"')
    ):
        version = if_none_match[1:-1]
        logger.debug("version={}", version)
        if version is not None:
            try:
                if int(version) == mitarbeiter.version:
                    return Response(status_code=status.HTTP_304_NOT_MODIFIED)
            except ValueError:
                logger.debug("invalid version={}", version)

    return JSONResponse(
        content=_mitarbeiter_to_dict(mitarbeiter),
        headers={ETAG: f'"{mitarbeiter.version}"'},
    )


@mitarbeiter_router.get(
    "",
    dependencies=[Depends(RolesRequired(Role.ADMIN))],
)
def get(
    request: Request,
    service: Annotated[MitarbeiterService, Depends(get_service)],
) -> JSONResponse:
    """Suche mit Query-Parameter."""
    query_params: Final = request.query_params
    log_str: Final = "{}"
    logger.debug(log_str, query_params)

    page: Final = query_params.get("page")
    size: Final = query_params.get("size")
    pageable: Final = Pageable.create(number=page, size=size)

    suchparameter = dict(query_params)
    if "page" in query_params:
        del suchparameter["page"]
    if "size" in query_params:
        del suchparameter["size"]

    mitarbeiter_slice: Final = service.find(
        suchparameter=suchparameter,
        pageable=pageable
    )

    result: Final = _mitarbeiter_slice_to_page(mitarbeiter_slice, pageable)
    logger.debug(log_str, result)
    return JSONResponse(content=result)


@mitarbeiter_router.get(
    "/nachnamen/{teil}",
    dependencies=[Depends(RolesRequired(Role.ADMIN))],
)
def get_nachnamen(
    teil: str,
    service: Annotated[MitarbeiterService, Depends(get_service)],
) -> JSONResponse:
    """Suche Nachnamen zum gegebenen Teilstring."""
    logger.debug("teil={}", teil)
    nachnamen: Final = service.find_nachnamen(teil=teil)
    return JSONResponse(content=nachnamen)


def _mitarbeiter_slice_to_page(
    mitarbeiter_slice: Slice[MitarbeiterDTO],
    pageable: Pageable,
) -> dict[str, Any]:
    mitarbeiter_dict: Final = tuple(
        _mitarbeiter_to_dict(mitarbeiter) for mitarbeiter in mitarbeiter_slice.content
    )
    page: Final = Page.create(
        content=mitarbeiter_dict,
        pageable=pageable,
        total_elements=mitarbeiter_slice.total_elements,
    )
    return asdict(obj=page)


def _mitarbeiter_to_dict(mitarbeiter: MitarbeiterDTO) -> dict[str, Any]:
    # https://docs.python.org/3/library/dataclasses.html
    mitarbeiter_dict: Final = asdict(obj=mitarbeiter)
    mitarbeiter_dict.pop("version")
    mitarbeiter_dict.update({"geburtsdatum": mitarbeiter.eintrittsdatum.isoformat()})
    return mitarbeiter_dict
