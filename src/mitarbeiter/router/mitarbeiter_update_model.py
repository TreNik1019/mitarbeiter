"""Pydantic-Model zum Aktualisieren eines Mitarbeiters."""

from datetime import date
from typing import Annotated, Any

from loguru import logger
from pydantic import BaseModel, ConfigDict, EmailStr, HttpUrl, StringConstraints

from mitarbeiter.entity.geschlecht import Geschlecht
from mitarbeiter.entity.mitarbeiter import Mitarbeiter
from mitarbeiter.entity.position import Position

__all__ = ["MitarbeiterUpdateModel"]


class MitarbeiterUpdateModel(BaseModel):
    """Pydantic-Model zum Aktualisieren eines Mitarbeiters."""

    nachname: Annotated[
        str,
        StringConstraints(
            pattern="^[A-ZÄÖÜ][a-zäöüß]+(-[A-ZÄÖÜ][a-zäöüß])?$",
            max_length=64,
        ),
    ]
    """Der Nachname."""
    email: EmailStr
    """Die eindeutige Emailadresse."""
    position: Position
    """Die Position im Unternehmen."""
    gehalt: float
    """Das Gehalt."""
    eintrittsdatum: date
    """Das Eintrittsdatum."""
    homepage: HttpUrl | None = None
    """Optionale Homepage."""
    geschlecht: Geschlecht | None = None
    """Optionales Geschlecht."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nachname": "Müller",
                "email": "test@acme.com",
                "position": "EN",
                "gehalt": 50000.0,
                "eintrittsdatum": "2020-01-15",
                "homepage": "https://www.mueller.de",
                "geschlecht": "M",
            },
        }
    )

    def to_dict(self) -> dict[str, Any]:
        """Konvertiert das Pydantic-Modell in ein Dictionary."""
        mitarbeiter_dict = self.model_dump()
        mitarbeiter_dict["id"] = None
        mitarbeiter_dict["werksausweis"] = None
        mitarbeiter_dict["auftraege"] = []
        mitarbeiter_dict["username"] = None
        mitarbeiter_dict["erzeugt"] = None
        mitarbeiter_dict["aktualisiert"] = None
        mitarbeiter_dict["homepage"] = str(mitarbeiter_dict["homepage"])
        return mitarbeiter_dict

    def to_mitarbeiter(self) -> Mitarbeiter:
        """Konvertierung in ein Mitarbeiter-Entity-Objekt."""
        logger.debug("self={}", self)
        mitarbeiter_dict = self.to_dict()

        mitarbeiter = Mitarbeiter(**mitarbeiter_dict)
        logger.debug("mitarbeiter={}", mitarbeiter)
        return mitarbeiter
