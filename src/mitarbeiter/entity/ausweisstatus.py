"""Enum für Ausweisstatus."""

from enum import StrEnum

import strawberry


@strawberry.enum
class Ausweisstatus(StrEnum):
    """Enum für Werksausweisstatus."""

    AKTIV = "A"
    """Aktiv."""

    GESPERRT = "G"
    """Gesperrt."""

    ABGELAUFEN = "B"
    """Abgelaufen."""
