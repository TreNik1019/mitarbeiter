"""Entity-Klasse für Auftrag."""

from datetime import date

from sqlalchemy import ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column, relationship

from mitarbeiter.entity.base import Base


class Auftrag(Base):
    """Entity-Klasse für Auftrag."""

    __tablename__ = "auftrag"

    id: Mapped[int] = mapped_column(
        Identity(start=1000),
        primary_key=True,
    )
    """Die ID des Auftrags."""

    bezeichnung: Mapped[str]
    """Die Bezeichnung des Auftrags."""

    auftragserteilung: Mapped[date]
    """Das Datum der Auftragserteilung."""

    dauer: Mapped[date]
    """Die Dauer des Auftrags."""

    mitarbeiter_id: Mapped[int] = mapped_column(
        ForeignKey("mitarbeiter.id"),
    )

    mitarbeiter: Mapped[Mitarbeiter] = relationship(  # noqa: F821 # ty: ignore[unresolved-reference] # pyright: ignore[reportUndefinedVariable ]
        back_populates="auftraege"
    )

    def __repr__(self) -> str:
        """Ausgabe des Auftrags als String."""
        return (
            f"Auftrag(id={self.id}, "
            f"bezeichnung={self.bezeichnung}, "
            f"auftragserteilung={self.auftragserteilung}, "
            f"dauer={self.dauer})"
        )
