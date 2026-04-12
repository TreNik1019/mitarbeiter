"""Pydantic-Model für die Auftraege."""

from datetime import date
from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

from mitarbeiter.entity import Auftrag

__all__ = ["AuftragModel"]


class AuftragModel(BaseModel):
    """Pydantic-Model für die Auftraege."""

    bezeichnung: Annotated[
        str,
        StringConstraints(
            pattern="^[A-ZÄÖÜ][a-zäöüß]+( [A-ZÄÖÜ][a-zäöüß]+)*$",
            max_length=128,
        ),
    ]
    """Die Bezeichnung des Auftrags."""
    auftragserteilung: date
    """Das Datum der Auftragserteilung."""
    dauer: date
    """Die Dauer des Auftrags."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "bezeichnung": "Projekt Alpha",
                "auftragserteilung": "2023-01-01",
                "dauer": "2023-12-31",
            },
        }
    )

    def to_auftrag(self) -> Auftrag:
        """Konvertiert das Pydantic-Modell in eine Entity."""
        auftrag_dict = self.model_dump()
        auftrag_dict["id"] = None
        auftrag_dict["mitarbeiter_id"] = None
        auftrag_dict["mitarbeiter"] = None
        return Auftrag(**auftrag_dict)
