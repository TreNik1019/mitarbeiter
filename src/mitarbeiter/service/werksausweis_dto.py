"""DTO für Werksausweis ."""

from dataclasses import dataclass
from datetime import date

import strawberry

from mitarbeiter.entity import Ausweisstatus, Werksausweis

__all__ = ["WerksausweisDTO"]


@dataclass(eq=False, slots=True, kw_only=True)
@strawberry.type
class WerksausweisDTO:
    """DTO-Klasse für den Werksausweis."""

    status: Ausweisstatus
    ausstellungsdatum: date
    guthaben: float

    def __init__(self, werksausweis: Werksausweis) -> None:
        """Objekt wird aus einem Werksausweis ersellt."""
        self.status = werksausweis.status
        self.ausstellungsdatum = werksausweis.ausstellungsdatum
        self.guthaben = werksausweis.guthaben
