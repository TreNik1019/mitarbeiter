"""DTO-Klasse für Mitarbeiterdaten."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal

import strawberry

from mitarbeiter.entity import Geschlecht, Mitarbeiter, Position

__all__ = ["MitarbeiterDTO"]


@dataclass(eq=False, slots=True, kw_only=True)
@strawberry.type
class MitarbeiterDTO:
    """DTO für den Mitarbeiter."""

    id: int
    version: int
    nachname: str
    email: str
    position: Position
    gehalt: Decimal
    eintrittsdatum: date
    homepage: str | None
    geschlecht: Geschlecht | None
    username: str

    def __init__(self, mitarbeiter: Mitarbeiter):
        """DTO aus dem Mitarbeiter erstellt."""
        self.id: int = mitarbeiter.id
        self.version: int = mitarbeiter.version
        self.nachname: str = mitarbeiter.nachname
        self.email: str = mitarbeiter.email
        self.position: Position = mitarbeiter.position
        self.gehalt: Decimal = mitarbeiter.gehalt
        self.eintrittsdatum: date = mitarbeiter.eintrittsdatum
        self.homepage: str | None = mitarbeiter.homepage
        self.geschlecht: Geschlecht | None = mitarbeiter.geschlecht
        self.username: str = mitarbeiter.username
