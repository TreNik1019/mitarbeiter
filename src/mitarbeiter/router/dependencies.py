# Copyright (C) 2025 - present Juergen Zimmermann, Hochschule Karlsruhe
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

"""Factory-Funktionen für Dependency Injection."""

from typing import Annotated

from fastapi import Depends

from mitarbeiter.repository.mitarbeiter_repository import MitarbeiterRepository
from mitarbeiter.security.dependencies import get_user_service
from mitarbeiter.security.user_service import UserService
from mitarbeiter.service.mitarbeiter_service import MitarbeiterService
from mitarbeiter.service.mitarbeiter_write_service import MitarbeiterWriteService


def get_repository() -> MitarbeiterRepository:
    """Factory-Funktion für MitarbeiterRepository.

    :return: Das Repository
    :rtype: MitarbeiterRepository
    """
    return MitarbeiterRepository()


def get_service(
    repo: Annotated[MitarbeiterRepository, Depends(get_repository)],
) -> MitarbeiterService:
    """Factory-Funktion für MitarbeiterService."""
    return MitarbeiterService(repo=repo)


def get_write_service(
    repo: Annotated[MitarbeiterRepository, Depends(get_repository)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> MitarbeiterWriteService:
    """Factory-Funktion für MitarbeiterWriteService."""
    return MitarbeiterWriteService(repo=repo, user_service=user_service)
