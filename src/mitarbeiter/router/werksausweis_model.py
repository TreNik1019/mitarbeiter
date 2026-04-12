"""Pydantic-Model für den Werksausweis."""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from mitarbeiter.entity import Ausweisstatus, Werksausweis

__all__ = ["WerksausweisModel"]


class WerksausweisModel(BaseModel):
    """Pydantic-Model für den Werksausweis."""

    status: Ausweisstatus | None = None
    """Der Status des Werksausweises."""
    ausstellungsdatum: str
    """Das Ausstellungsdatum des Ausweises."""
    guthaben: Annotated[float, Field(strict=True, ge=0.0, le=500.0)]
    """Das Guthaben auf dem Ausweis."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "A",
                "ausstellungsdatum": "2023-01-01",
                "guthaben": 100.0,
            },
        }
    )

    def to_werksausweis(self) -> Werksausweis:
        """Konvertiert das Pydantic-Modell in ein Werksausweis-Objekt."""
        werksausweis_dict = self.model_dump()
        werksausweis_dict["id"] = None
        werksausweis_dict["mitarbeiter_id"] = None
        werksausweis_dict["mitarbeiter"] = None

        return Werksausweis(**werksausweis_dict)
