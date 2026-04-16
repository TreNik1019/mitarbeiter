"""Geschäftslogik zum Schreiben von Mitarbeiterdaten."""

from typing import Final

from loguru import logger

from mitarbeiter.entity import Mitarbeiter
from mitarbeiter.repository import MitarbeiterRepository, Session
from mitarbeiter.security import User, UserService
from mitarbeiter.service.exceptions import (
    EmailExistsError,
    NotFoundError,
    UsernameExistsError,
    VersionOutdatedError,
)
from mitarbeiter.service.mailer import send_mail
from mitarbeiter.service.mitarbeiter_dto import MitarbeiterDTO

__all__ = ["MitarbeiterWriteService"]


class MitarbeiterWriteService:
    """Service-Klasse mit Geschäftslogik für Mitarbeiter."""

    def __init__(self, repo: MitarbeiterRepository, user_service: UserService) -> None:
        """Konstruktor mit abhängigem MitarbeiterRepository und UserService."""
        self.repo: MitarbeiterRepository = repo
        self.user_service: UserService = user_service

    def create(self, mitarbeiter: Mitarbeiter) -> MitarbeiterDTO:
        """Neuen Mitarbeiter anlegen.

        :param mitarbeiter: Der neue Mitarbeiter ohne ID
        :return: Der neu angelegte Mitarbeiter mit generierter ID
        :rtype: Rückgabetyp MitarbeiterDTO
        :raises EmailExistsError, wenn Emailadresse schon existiert
        :raises UsernameExistsError, wenn Username schon existiert
        """
        logger.debug(
            "mitarbeiter={}, werksausweis={}, auftraege={}",
            mitarbeiter,
            mitarbeiter.werksausweis,
            mitarbeiter.auftraege,
        )

        username: Final = mitarbeiter.username
        if username is None:
            raise ValueError
        # security muss noch gemacht werden username_exists und email_exists
        if self.user_service.username_exists(username):
            raise UsernameExistsError(username)

        email: Final = mitarbeiter.email
        if self.user_service.email_exists(email):
            raise EmailExistsError(email=email)

        user: Final = User(
            username=username,
            email=mitarbeiter.email,
            nachname=mitarbeiter.nachname,
            vorname=mitarbeiter.nachname,
            password="p",  # noqa: S106 # NOSONAR
            roles=[],
        )
        # security...
        user_id = self.user_service.create_user(user)
        logger.debug("user_id={}", user_id)

        with Session() as session:
            if self.repo.exists_email(email=email, session=session):
                raise EmailExistsError(email=email)

            mitarbeiter_db: Final = self.repo.create(
                mitarbeiter=mitarbeiter, session=session
            )
            mitarbeiter_dto: Final = MitarbeiterDTO(mitarbeiter_db)
            session.commit()

        # TODO User aus Keycloak loeschen, falls die DB-Transaktion fehlschlaegt

        send_mail(mitarbeiter_dto=mitarbeiter_dto)
        logger.debug("mitarbeiter_dto={}", mitarbeiter_dto)
        return mitarbeiter_dto

    def update(
        self, mitarbeiter: Mitarbeiter, mitarbeiter_id: int, version: int
    ) -> MitarbeiterDTO:
        """Daten eines Mitarbeiters ändern.

        :param mitarbeiter: Neuen Daten
        :param mitarbeiter_id: ID des Mitarbeiters der aktualisiert werden soll
        :param version: Version für optimistische Synchronisation
        :return: Aktualisierte Mitarbeiter
        :rtype: Typ->MitarbeiterDTO
        :raises NotFoundError: Falls der Mitarbeiter mit der ID nicht gefunden wird
        :raises VersionOutdatedError: Verion ist nicht mehr aktuell
        :raises EmailExistsError: Emailadresse existiert bereits
        """
        logger.debug(
            "mitarbeiter_id={},version={}, {}", mitarbeiter_id, version, mitarbeiter
        )

        with Session() as session:
            if (
                mitarbeiter_db := self.repo.find_by_id(
                    mitarbeiter_id=mitarbeiter_id, session=session
                )
            ) is None:
                raise NotFoundError(mitarbeiter_id)
            if mitarbeiter_db.version > version:
                raise VersionOutdatedError(version)

            email: Final = mitarbeiter.email
            if email != mitarbeiter_db.email and self.repo.exists_email_other_id(
                mitarbeiter_id=mitarbeiter_id,
                email=email,
                session=session,
            ):
                raise EmailExistsError(email)

            mitarbeiter_db.set(mitarbeiter)
            if (
                mitarbeiter_updated := self.repo.update(
                    mitarbeiter=mitarbeiter_db, session=session
                )
            ) is None:
                raise NotFoundError(mitarbeiter_id)
            mitarbeiter_dto: Final = MitarbeiterDTO(mitarbeiter_updated)
            logger.debug("{}", mitarbeiter_dto)

            session.commit()
            mitarbeiter_dto.version += 1
            return mitarbeiter_dto

    def delete_by_id(self, mitarbeiter_id: int) -> None:
        """Einen Mitarbeiter anhand seiner ID löschen."""
        logger.debug("mitarbeiter_id={}", mitarbeiter_id)
        with Session() as session:
            self.repo.delete_by_id(mitarbeiter_id=mitarbeiter_id, session=session)
            session.commit()
