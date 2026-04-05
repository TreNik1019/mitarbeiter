"""Modul für den DB-Zugriff."""

from mitarbeiter.repository.mitarbeiter_repository import MitarbeiterRepository
from mitarbeiter.repository.pageable import MAX_PAGE_SIZE, Pageable
from mitarbeiter.repository.session_factory import Session, engine
from mitarbeiter.repository.slice import Slice

__all__ = [
    "MAX_PAGE_SIZE",
    "MitarbeiterRepository",
    "Pageable",
    "Session",
    "Slice",
    "engine",
]
