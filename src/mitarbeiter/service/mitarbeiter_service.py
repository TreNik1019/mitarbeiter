"""Geschäftslogik zum Lesen von Mitarbeiterdaten."""

from collections.abc import Mapping, Sequence
from typing import Final

from loguru import logger

from mitarbeiter.repository import (
    MitarbeiterRepository,
    Pageable,
    Session,
    Slice,
)
from mitarbeiter.security import Role, User
from mitarbeiter.service.exceptions import ForbiddenError, NotFoundError
from mitarbeiter.service.mitarbeiter_dto import MitarbeiterDTO

__all__ = ["MitarbeiterService"]


class MitarbeiterService:
    """Service-Klasse zum Lesen von Mitarbeiterdaten."""

    def __init__(self, repo: MitarbeiterRepository) -> None:
        """Konstruktor mit Dependency Injection."""
        self.repo: MitarbeiterRepository = repo

    def find_by_id(self, mitarbeiter_id: int, current_user: User) -> MitarbeiterDTO:
        """Suche mit Mitarbeiter-ID."""
        logger.debug(
            "mitarbeiter_id={}", "current_user={}", mitarbeiter_id, current_user
        )

        with Session() as session:
            user_is_admin: Final = Role.ADMIN in current_user.roles

            if (
                mitarbeiter := self.repo.find_by_id(
                    mitarbeiter_id=mitarbeiter_id,
                    session=session,
                )
            ) is None:
                if user_is_admin:
                    message: Final = (
                        f"Kein Mitarbeiter mit der ID  {mitarbeiter_id} gefunden"
                    )
                    logger.debug("NotFoundError: {}", message)
                    raise NotFoundError(mitarbeiter_id=mitarbeiter_id)
                logger.debug("Keine Berechtigung")
                raise ForbiddenError

            if mitarbeiter.username != current_user.username and not user_is_admin:
                logger.debug(
                    "mitarbeiter.username={}, user.username={}, user.roles={}",
                    mitarbeiter.username,
                    current_user.username,
                    current_user.roles,
                )
                raise ForbiddenError

            mitarbeiter_dto: Final = MitarbeiterDTO(mitarbeiter)
            session.commit()

        logger.debug("{}", mitarbeiter_dto)
        return mitarbeiter_dto

    def find(
        self,
        suchparameter: Mapping[str, str],
        pageable: Pageable,
    ) -> Slice[MitarbeiterDTO]:
        """Suche mit Suchparametern."""
        logger.debug("{}", suchparameter)
        with Session() as session:
            mitarbeiter_slice: Final = self.repo.find(
                suchparameter=suchparameter, pageable=pageable, session=session
            )
            if len(mitarbeiter_slice.content) == 0:
                raise NotFoundError(suchparameter=suchparameter)

            mitarbeiter_dto: Final = tuple(
                MitarbeiterDTO(mitarbeiter) for mitarbeiter in mitarbeiter_slice.content
            )
            session.commit()

        mitarbeiter_dto_slice = Slice(
            content=mitarbeiter_dto, total_elements=mitarbeiter_slice.total_elements
        )
        logger.debug("{}", mitarbeiter_dto_slice)
        return mitarbeiter_dto_slice

    def find_nachnamen(self, teil: str) -> Sequence[str]:
        """Suche Nachnamen zu einem Teilstring."""
        logger.debug("teil={}", teil)
        with Session() as session:
            nachnamen: Final = self.repo.find_nachnamen(teil=teil, session=session)
            session.commit()

        logger.debug("{}", nachnamen)
        if len(nachnamen) == 0:
            raise NotFoundError
        return nachnamen
