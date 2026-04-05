"""Modul für die REST-Schnittstelle einschließlich Validierung."""

from collections.abc import Sequence

from mitarbeiter.router.health_router import liveness, readiness
from mitarbeiter.router.health_router import router as health_router
from mitarbeiter.router.mitarbeiter_router import (
    get,
    get_by_id,
    get_nachnamen,
    mitarbeiter_router,
)
from mitarbeiter.router.mitarbeiter_write_router import (
    delete_by_id,
    mitarbeiter_write_router,
    post,
    put,
)
from mitarbeiter.router.shutdown_router import router as shutdown_router
from mitarbeiter.router.shutdown_router import shutdown

__all__: Sequence[str] = [
    "delete_by_id",
    "get",
    "get_by_id",
    "get_nachnamen",
    "health_router",
    "liveness",
    "mitarbeiter_router",
    "mitarbeiter_write_router",
    "post",
    "put",
    "readiness",
    "shutdown",
    "shutdown_router",
]
