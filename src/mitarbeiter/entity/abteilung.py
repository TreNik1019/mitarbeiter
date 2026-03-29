# Copyright (C) 2022 - present Juergen Zimmermann, Hochschule Karlsruhe
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Entity-Klasse für Abteilung."""

from sqlalchemy.orm import Mapped, mapped_column

from mitarbeiter.entity.base import Base


class Abteilung(Base):
    """Entity-Klasse für Abteilung."""

    __tablename__ = "abteilung"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    """Die ID der Abteilung."""

    name: Mapped[str]
    """Der Name der Abteilung."""

    standort: Mapped[str]
    """Der Standort der Abteilung."""

    def __repr__(self) -> str:
        """Ausgabe der Abteilung als String."""
        return (
            f"Abteilung(id={self.id}, name={self.name}, "
            + f"standort={self.standort})"
        )
