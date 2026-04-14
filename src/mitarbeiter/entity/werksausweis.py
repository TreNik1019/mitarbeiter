# Copyright (C) 2022 - present Juergen Zimmermann, Hochschule Karlsruhe
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License ...

"""Entity-Klasse für den Werksausweis."""

from datetime import date

from sqlalchemy import ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column, relationship

from mitarbeiter.entity.ausweisstatus import Ausweisstatus
from mitarbeiter.entity.base import Base


class Werksausweis(Base):
    """Entity-Klasse für den Werksausweis."""

    __tablename__ = "werksausweis"

    # =========================
    # Attribute
    # =========================

    status: Mapped[Ausweisstatus]
    """Der Status des Werksausweises."""

    ausstellungsdatum: Mapped[date]
    """Das Ausstellungsdatum des Ausweises."""

    guthaben: Mapped[float]
    """Das Guthaben auf dem Ausweis."""

    id: Mapped[int] = mapped_column(
        Identity(start=1000),
        primary_key=True,
    )
    """Primärschlüssel."""

    # =========================
    # Relationship (1:1 zu Mitarbeiter)
    # =========================

    mitarbeiter_id: Mapped[int] = mapped_column(
        ForeignKey("mitarbeiter.id"),
    )

    mitarbeiter: Mapped[Mitarbeiter] = relationship(  # noqa: F821 # ty: ignore[unresolved-reference] # pyright: ignore[reportUndefinedVariable]
        back_populates="werksausweis",
    )

    # =========================
    # Methoden
    # =========================

    def __repr__(self) -> str:
        """Ausgabe des Werksausweises als String."""
        return (
            f"Werksausweis(id={self.id}, status={self.status}, "
            f"ausstellungsdatum={self.ausstellungsdatum}, "
            f"guthaben={self.guthaben})"
        )
