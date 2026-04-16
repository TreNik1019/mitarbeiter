"""DTO für Auftrag."""

from dataclasses import dataclass
from datetime import date

import strawberry

from mitarbeiter.entity import Auftrag


@dataclass(eq=False, slots=True, kw_only=True)
@strawberry.type
class AuftragDTO:
    """DTO-Klasse für den Auftrag."""

    bezeichnung: str
    auftragserteilung: date
    dauer: date

    def __init__(self, auftrag: Auftrag) -> None:
        """DTO wird aus einem Auftrag erstellt."""
        self.bezeichnung = auftrag.bezeichnung
        self.auftragserteilung = auftrag.auftragserteilung
        self.dauer = auftrag.dauer
