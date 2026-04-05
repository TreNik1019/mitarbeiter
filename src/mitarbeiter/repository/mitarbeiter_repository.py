"""Repository fuer persistente Mitarbeiterdaten."""

# "list" ist eine mutable "Sequence"
# https://docs.python.org/3/library/stdtypes.html#lists
# https://docs.python.org/3/library/stdtypes.html#typesseq
from collections.abc import Mapping
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
        """Suche mit der Mitarbeiter-ID."""
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
        """Suche mit Suchparameter."""
        log_str: Final = "{}"
        logger.debug(log_str, suchparameter)
        if not suchparameter:
            return self._find_all(pageable=pageable, session=session)

        # Iteration ueber die Schluessel des Dictionaries mit den Suchparameter
        for key, value in suchparameter.items():
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
        # https://docs.sqlalchemy.org/en/20/orm/session_basics.html#querying
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
            total_elements=anzahl
        )
        logger.debug("mitarbeiter_slice={}", mitarbeiter_slice)
        return mitarbeiter_slice

    def _count_all_rows(self, session: Session) -> int:
        statement: Final = select(func.count()).select_from(Mitarbeiter)
        count: Final = session.execute(statement).scalar()
        return count if count is not None else 0

    def _find_by_nachname(
        self,
        teil: str,
        pageable: Pageable,
        session: Session,
    ) -> Slice[Mitarbeiter]:
        logger.debug("teil={}", teil)
        offset = pageable.number * pageable.size
        # https://docs.sqlalchemy.org/en/20/orm/session_basics.html#querying
        statement: Final = (
            (
                select(Mitarbeiter)
                .options(joinedload(Mitarbeiter.werksausweis))
                .filter(Mitarbeiter.nachname.ilike(f"%{teil}%"))
                .limit(pageable.size)
                .offset(offset)
            )
            if pageable.size != 0
            else (
                select(Mitarbeiter)
                .options(joinedload(Mitarbeiter.werksausweis))
                .filter(Mitarbeiter.nachname.ilike(f"%{teil}%"))
            )
        )
        mitarbeiter: Final = session.scalars(statement).all()
        anzahl: Final = self._count_rows_nachname(teil, session)
        mitarbeiter_slice: Final = Slice(
            content=tuple(mitarbeiter),
            total_elements=anzahl
        )
        logger.debug("{}", mitarbeiter_slice)
        return mitarbeiter_slice

    def _count_rows_nachname(self, teil: str, session: Session) -> int:
        statement: Final = (
            select(func.count())
            .select_from(Mitarbeiter)
            .filter(Mitarbeiter.nachname.ilike(f"%{teil}%"))
        )
        count: Final = session.execute(statement).scalar()
        return count if count is not None else 0
