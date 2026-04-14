# Copyright (C) 2022 - present Juergen Zimmermann, Hochschule Karlsruhe
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License ...

"""Entity-Klasse für Mitarbeiterdaten."""

from datetime import date, datetime
from decimal import Decimal
from typing import Any, Self

from sqlalchemy import Identity, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from mitarbeiter.entity.auftrag import Auftrag
from mitarbeiter.entity.base import Base
from mitarbeiter.entity.geschlecht import Geschlecht
from mitarbeiter.entity.position import Position
from mitarbeiter.entity.werksausweis import Werksausweis


class Mitarbeiter(Base):
    """Entity-Klasse für Mitarbeiterdaten."""

    __tablename__ = "mitarbeiter"

    # =========================
    # Primitive Felder
    # =========================

    nachname: Mapped[str]
    """Der Nachname."""

    email: Mapped[str] = mapped_column(unique=True)
    """Die eindeutige Emailadresse."""

    position: Mapped[Position]
    """Die Position im Unternehmen."""

    gehalt: Mapped[Decimal]
    """Das Gehalt."""

    eintrittsdatum: Mapped[date]
    """Das Eintrittsdatum."""

    homepage: Mapped[str | None]
    """Optionale Homepage."""

    geschlecht: Mapped[Geschlecht | None]
    """Optionales Geschlecht."""

    username: Mapped[str]
    """Login-Username."""

    # =========================
    # ID
    # =========================

    id: Mapped[int] = mapped_column(
        Identity(start=1000),
        primary_key=True,
    )
    """Primärschlüssel."""

    # =========================
    # Relations
    # =========================

    auftraege: Mapped[list[Auftrag]] = relationship(
        back_populates="mitarbeiter",
        cascade="save-update, delete",
    )

    werksausweis: Mapped[Werksausweis] = relationship(
        back_populates="mitarbeiter",
        innerjoin=True,
        cascade="save-update, delete",
    )

    # =========================
    # Versioning
    # =========================

    version: Mapped[int] = mapped_column(
        nullable=False,
        default=0,
    )
    """Version für Optimistic Locking."""

    # =========================
    # Timestamp
    # =========================

    erzeugt: Mapped[datetime | None] = mapped_column(
        insert_default=func.now(),
        default=None,
    )

    aktualisiert: Mapped[datetime | None] = mapped_column(
        insert_default=func.now(),
        onupdate=func.now(),
        default=None,
    )

    # =========================
    # Methoden
    # =========================
    def set(self, mitarbeiter: Self) -> None:
        """Primitive Attributwerte überschreiben, z.B. vor DB-Update.

        :param patient: Mitarbeiter-Objekt mit den aktuellen Daten
        """
        self.nachname = mitarbeiter.nachname
        self.email = mitarbeiter.email
        self.position = mitarbeiter.position
        self.gehalt = mitarbeiter.gehalt
        self.eintrittsdatum = mitarbeiter.eintrittsdatum

    def __eq__(self, other: Any) -> bool:
        """Vergleich auf Gleicheit, ohne Joins zu verursachen."""
        # Vergleich der Referenzen: id(self) == id(other)
        if self is other:
            return True
        if not isinstance(other, type(self)):
            return False
        return self.id is not None and self.id == other.id

    def __hash__(self) -> int:
        """Hash-Funktion anhand der ID, ohne Joins zu verursachen."""
        return hash(self.id) if self.id is not None else hash(type(self))

    def __repr__(self) -> str:
        """Ausgabe eines Mitarbeiters als String, ohne Joins zu verursachen."""
        return (
            f"Mitarbeiter(id={self.id}, version={self.version}, "
            f"nachname={self.nachname}, email={self.email}, "
            f"position={self.position}, gehalt={self.gehalt}, "
            f"eintrittsdatum={self.eintrittsdatum})"
        )
