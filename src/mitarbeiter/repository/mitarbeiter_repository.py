"""Repository fuer persistente Mitarbeiterdaten."""

# "list" ist eine mutable "Sequence"
# https://docs.python.org/3/library/stdtypes.html#lists
# https://docs.python.org/3/library/stdtypes.html#typesseq
from collections.abc import Mapping, Sequence
from typing import Final

from loguru import logger
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from mitarbeiter.entity import Mitarbeiter
from mitarbeiter.repository.pageable import Pageable
from mitarbeiter.repository.slice import Slice

__all__: list[str] = ["MitarbeiterRepository"]


class MitarbeiterRepository:
    """Repository-Klasse mit CRUD-Methoden für die Entity-Klasse Mitarbeiter."""

    def find_by_id(
        self,
        mitarbeiter_id: int | None,
        session: Session
    ) -> Mitarbeiter | None:
        """Find a mitarbeiter by ID."""
        logger.debug("mitarbeiter_id={}", mitarbeiter_id)  # NOSONAR

        if mitarbeiter_id is None:
            return None

        statement: Final = (
            select(Mitarbeiter)
            .options(joinedload(Mitarbeiter.werksausweis))
            .where(Mitarbeiter.id == mitarbeiter_id)
        )
        mitarbeiter: Final = session.scalar(statement)

        logger.debug("{}", mitarbeiter)
        return mitarbeiter

    def find(
        self,
        suchparameter: Mapping[str, str],
        pageable: Pageable,
        session: Session,
    ) -> Slice[Mitarbeiter]:
        """Suche mit Suchparametern."""
        log_str: Final = "{}"
        logger.debug(log_str, suchparameter)
        if not suchparameter:
            return self._find_all(pageable=pageable, session=session)

        for key, value in suchparameter.items():
            if key == "email":
                mitarbeiter = self._find_by_email(email=value, session=session)
                logger.debug(log_str, mitarbeiter)
                return (
                    Slice(content=(mitarbeiter,), total_elements=1)
                    if mitarbeiter is not None
                    else Slice(content=(), total_elements=0)
                )
            if key == "nachname":
                mitarbeiter = self._find_by_nachname(
                    teil=value, pageable=pageable, session=session
                )
                logger.debug(log_str, mitarbeiter)
                return mitarbeiter
        return Slice(content=(), total_elements=0)

    def _find_all(self, pageable: Pageable, session: Session) -> Slice[Mitarbeiter]:
        logger.debug("aufgerufen")
        offset = pageable.number * pageable.size
        statement: Final = (
            (
                select(Mitarbeiter)
                .options(joinedload(Mitarbeiter.werksausweis))
                .limit(pageable.size)
                .offset(offset)
            )
            if pageable.size != 0
            else (select(Mitarbeiter).options(joinedload(Mitarbeiter.werksausweis)))
        )
        mitarbeiter: Final = (session.scalars(statement)).all()
        anzahl: Final = self._count_all_rows(session)
        mitarbeiter_slice: Final = Slice(
            content=tuple(mitarbeiter),
            total_elements=anzahl,
        )
        logger.debug("mitarbeiter_slice={}", mitarbeiter_slice)
        return mitarbeiter_slice

    def _count_all_rows(self, session: Session) -> int:
        statement: Final = select(func.count()).select_from(Mitarbeiter)
        count: Final = session.execute(statement).scalar()
        return count if count is not None else 0

    def _find_by_email(self, email: str, session: Session) -> Mitarbeiter | None:
        """Einen Mitarbeiter anhand der Emailadresse suchen."""
        logger.debug("email={}", email)  # NOSONAR
        statement: Final = (
            select(Mitarbeiter)
            .options(joinedload(Mitarbeiter.werksausweis))
            .where(Mitarbeiter.email == email)
        )
        mitarbeiter: Final = session.scalar(statement)
        logger.debug("{}", mitarbeiter)
        return mitarbeiter

    def _find_by_nachname(
        self,
        teil: str,
        pageable: Pageable,
        session: Session,
    ) -> Slice[Mitarbeiter]:
        logger.debug("teil={}", teil)
        offset = pageable.number * pageable.size
        statement: Final = (
            (
                select(Mitarbeiter)
                .options(joinedload(Mitarbeiter.werksausweis))
                .where(Mitarbeiter.nachname.ilike(f"%{teil}%"))
                .limit(pageable.size)
                .offset(offset)
            )
            if pageable.size != 0
            else (
                select(Mitarbeiter)
                .options(joinedload(Mitarbeiter.werksausweis))
                .where(Mitarbeiter.nachname.ilike(f"%{teil}%"))
            )
        )
        mitarbeiter: Final = session.scalars(statement).all()
        anzahl: Final = self._count_rows_nachname(teil, session)
        mitarbeiter_slice: Final = Slice(
            content=tuple(mitarbeiter),
            total_elements=anzahl,
        )
        logger.debug("{}", mitarbeiter_slice)
        return mitarbeiter_slice

    def _count_rows_nachname(self, teil: str, session: Session) -> int:
        statement: Final = (
            select(func.count())
            .select_from(Mitarbeiter)
            .where(Mitarbeiter.nachname.ilike(f"%{teil}%"))
        )
        count: Final = session.execute(statement).scalar()
        return count if count is not None else 0

    def exists_email(self, email: str, session: Session) -> bool:
        """Abfrage, ob es die Emailadresse bereits gibt."""
        logger.debug("email={}", email)

        statement: Final = select(func.count()).where(Mitarbeiter.email == email)
        anzahl: Final = session.scalar(statement)
        logger.debug("anzahl={}", anzahl)
        return anzahl is not None and anzahl > 0

    def find_nachnamen(self, teil: str, session: Session) -> Sequence[str]:
        """Suche Nachnamen zu einem Teilstring."""
        logger.debug("teil={}", teil)

        statement: Final = (
            select(Mitarbeiter.nachname)
            .filter(Mitarbeiter.nachname.ilike(f"%{teil}%"))
            .distinct()
        )
        nachnamen: Final = (session.scalars(statement)).all()

        logger.debug("nachnamen={}", nachnamen)
        return nachnamen
