"""Enum für Rollen."""

from enum import StrEnum


class Role(StrEnum):
    """Enum für Rollen."""

    ADMIN = "ADMIN"
    """Rolle für die Administration."""

    MITARBEITER = "MITARBEITER"
    """Rolle für registrierten Mitarbeiter."""
