"""DTO für Abteilung ."""
from dataclasses import dataclass

import strawberry

from mitarbeiter.entity import Abteilung


@dataclass(eq=False, slots=True, kw_only=True)
@strawberry.type
class AbteilungDTO:
    """DTO-Klasse für die Abteilung."""

    name: str
    standort: str

    def __init__(self, abteilung: Abteilung) -> None:
        """DTO wird aus einer Abteilung ersellt."""
        self.name = abteilung.name
        self.standort = abteilung.standort
