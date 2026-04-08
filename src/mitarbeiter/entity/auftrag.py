"""Entity-Klasse für Auftrag."""

from datetime import date

from sqlalchemy.orm import Mapped, mapped_column

from mitarbeiter.entity.base import Base


class Auftrag(Base):
    """Entity-Klasse für Auftrag."""

    __tablename__ = "auftrag"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    """Die ID des Auftrags."""

    bezeichnung: Mapped[str]
    """Die Bezeichnung des Auftrags."""

    auftragserteilung: Mapped[date]
    """Das Datum der Auftragserteilung."""

    dauer: Mapped[date]
    """Die Dauer des Auftrags."""

    def __repr__(self) -> str:
        """Ausgabe des Auftrags als String."""
        return (
            f"Auftrag(id={self.id}, "
            f"bezeichnung={self.bezeichnung}, "
            f"auftragserteilung={self.auftragserteilung}, "
            f"dauer={self.dauer})"
        )
