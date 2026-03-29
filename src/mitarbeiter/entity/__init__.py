"""Modul für persistente Mitarbeiter-Objekte."""

from mitarbeiter.entity.abteilung import Abteilung
from mitarbeiter.entity.ausweisstatus import Ausweisstatus
from mitarbeiter.entity.geschlecht import Geschlecht
from mitarbeiter.entity.mitarbeiter import Mitarbeiter
from mitarbeiter.entity.position import Position
from mitarbeiter.entity.werksausweis import Werksausweis

__all__ = [
    "Abteilung",
    "Ausweisstatus",
    "Geschlecht",
    "Mitarbeiter",
    "Position",
    "Werksausweis",
    ]
