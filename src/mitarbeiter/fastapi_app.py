"""MainApp."""

from contextlib import asynccontextmanager
from pathlib import Path
from time import time
from typing import TYPE_CHECKING, Any, Final

from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.gzip import (
    GZipMiddleware,  # https://fastapi.tiangolo.com/advanced/middleware/#gzipmiddleware
)
from fastapi.responses import FileResponse
from loguru import logger
from prometheus_fastapi_instrumentator import Instrumentator

from mitarbeiter.banner import banner
from mitarbeiter.config import (
    dev_db_populate,
    dev_keycloak_populate,
)
from mitarbeiter.config.dev.db_populate import db_populate
from mitarbeiter.config.dev.db_populate_router import router as db_populate_router
from mitarbeiter.config.dev.keycloak_populate import keycloak_populate
from mitarbeiter.config.dev.keycloak_populate_router import (
    router as keycloak_populate_router,
)
from mitarbeiter.graphql_api import graphql_router
from mitarbeiter.problem_details import create_problem_details
from mitarbeiter.repository.session_factory import engine
from mitarbeiter.router import (
    health_router,
    mitarbeiter_router,
    mitarbeiter_write_router,
    shutdown_router,
)
from mitarbeiter.security import AuthorizationError, LoginError, set_response_headers
from mitarbeiter.security import router as auth_router
from mitarbeiter.service import (
    EmailExistsError,
    ForbiddenError,
    NotFoundError,
    UsernameExistsError,
    VersionOutdatedError,
)

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator, Awaitable, Callable

__all__ = [
    "email_exists_error_handler",
    "forbidden_error_handler",
    "not_found_error_handler",
    "username_exists_error_handler",
    "version_outdated_error_handler",
]


TEXT_PLAIN: Final = "text/plain"


# --------------------------------------------------------------------------------------
# S t a r t u p   u n d   S h u t d o w n
# --------------------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:  # noqa: RUF029
    """DB und Keycloak neu laden, falls im dev-Modus, sowie Banner in der Konsole."""
    if dev_db_populate:
        db_populate()
    if dev_keycloak_populate:
        keycloak_populate()
    banner(app.routes)
    yield
    logger.info("Der Server wird heruntergefahren")
    logger.info("Connection-Pool fuer die DB wird getrennt.")
    engine.dispose()


app: Final = FastAPI(lifespan=lifespan)

Instrumentator().instrument(app).expose(app)

app.add_middleware(GZipMiddleware, minimum_size=500)  # ty:ignore[invalid-argument-type]


@app.middleware("http")
async def log_request_header(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    logger.debug(f"{request.method} '{request.url}'")
    return await call_next(request)


@app.middleware("http")
async def log_response_time(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    start = time()
    response = await call_next(request)
    duration_ms = (time() - start) * 1000
    logger.debug(
        f"Response time: {duration_ms:.2f} ms, statuscode: {response.status_code}"
    )
    return response


# --------------------------------------------------------------------------------------
# R E S T
# --------------------------------------------------------------------------------------
app.include_router(mitarbeiter_router, prefix="/rest")
app.include_router(mitarbeiter_write_router, prefix="/rest")
app.include_router(auth_router, prefix="/auth")
app.include_router(health_router, prefix="/health")
app.include_router(shutdown_router, prefix="/admin")

if dev_db_populate:
    app.include_router(db_populate_router, prefix="/dev")
if dev_keycloak_populate:
    app.include_router(keycloak_populate_router, prefix="/dev")


# --------------------------------------------------------------------------------------
# G r a p h Q L
# --------------------------------------------------------------------------------------
app.include_router(graphql_router, prefix="/graphql")


# --------------------------------------------------------------------------------------
# S e c u r i t y
# --------------------------------------------------------------------------------------
@app.middleware("http")
async def add_security_headers(
    request: Request,
    call_next: Callable[[Any], Awaitable[Response]],
) -> Response:
    """Header-Daten beim Response für IT-Sicherheit setzen."""
    response: Final[Response] = await call_next(request)
    set_response_headers(response)
    return response


# --------------------------------------------------------------------------------------
# F a v i c o n
# --------------------------------------------------------------------------------------
@app.get("/favicon.ico")
def favicon() -> FileResponse:
    """facicon.ico ermitteln."""
    src_path: Final = Path("src")
    file_name: Final = "favicon.ico"
    favicon_path: Final = Path("mitarbeiter") / "static" / file_name
    file_path: Final = src_path / favicon_path if src_path.is_dir() else favicon_path
    logger.debug("file_path={}", file_path)
    return FileResponse(
        path=file_path,
        headers={"Content-Disposition": f"attachment; filename={file_name}"},
    )


# --------------------------------------------------------------------------------------
# E x c e p t i o n   H a n d l e r
# --------------------------------------------------------------------------------------
@app.exception_handler(NotFoundError)
def not_found_error_handler(_request: Request, _err: NotFoundError) -> Response:
    """Errorhandler für NotFoundError."""
    return create_problem_details(status_code=status.HTTP_404_NOT_FOUND)


@app.exception_handler(ForbiddenError)
def forbidden_error_handler(_request: Request, _err: ForbiddenError) -> Response:
    """Errorhandler für ForbiddenError."""
    return create_problem_details(status_code=status.HTTP_403_FORBIDDEN)


@app.exception_handler(AuthorizationError)
def authorization_error_handler(
    _request: Request,
    _err: AuthorizationError,
) -> Response:
    """Errorhandler für AuthorizationError."""
    return create_problem_details(status_code=status.HTTP_401_UNAUTHORIZED)


@app.exception_handler(LoginError)
# pylint: disable-next=invalid-name
def login_error_handler(_request: Request, err: LoginError) -> Response:
    """Exception-Handler, wenn der Benutzername oder das Passwort fehlerhaft ist."""
    return create_problem_details(
        status_code=status.HTTP_401_UNAUTHORIZED, detail=str(err)
    )


@app.exception_handler(EmailExistsError)
def email_exists_error_handler(_request: Request, err: EmailExistsError) -> Response:
    """Exception-Handling für EmailExistsError."""
    return create_problem_details(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=str(err),
    )


@app.exception_handler(UsernameExistsError)
def username_exists_error_handler(
    _request: Request,
    err: UsernameExistsError,
) -> Response:
    """Exception-Handling für UsernameExistsError."""
    return create_problem_details(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=str(err),
    )


@app.exception_handler(VersionOutdatedError)
def version_outdated_error_handler(
    _request: Request,
    err: VersionOutdatedError,
) -> Response:
    """Exception-Handling für VersionOutdatedError."""
    return create_problem_details(
        status_code=status.HTTP_412_PRECONDITION_FAILED,
        detail=str(err),
    )
