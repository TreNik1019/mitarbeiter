"""Pydantic Model für die Mitarbeiterdaten."""

from typing import Annotated, Final

from loguru import logger
from pydantic import StringConstraints

from mitarbeiter.entity import Mitarbeiter
from mitarbeiter.router.auftrag_model import AuftragModel
from mitarbeiter.router.mitarbeiter_update_model import MitarbeiterUpdateModel
from mitarbeiter.router.werksausweis_model import WerksausweisModel

__all__ = ["MitarbeiterModel"]


class MitarbeiterModel(MitarbeiterUpdateModel):
    """Pydantic Model für die Mitarbeiterdaten."""

    werksausweis: WerksausweisModel
    """Der zugehörige Werksausweis."""
    auftraege: list[AuftragModel]
    """Die zugehörigen Aufträge."""
    username: Annotated[str, StringConstraints(max_length=20)]

    def to_mitarbeiter(self) -> Mitarbeiter:
        """Konvertiert das Pydantic-Modell in eine Entity."""
        logger.debug("self={}", self)
        mitarbeiter_dict = self.to_dict()
        mitarbeiter_dict["username"] = self.username

        mitarbeiter: Final = Mitarbeiter(**mitarbeiter_dict)
        mitarbeiter.werksausweis = self.werksausweis.to_werksausweis()
        mitarbeiter.auftraege = [
            auftrag_model.to_auftrag() for auftrag_model in self.auftraege
        ]
        logger.debug("mitarbeiter={}", mitarbeiter)
        return mitarbeiter
