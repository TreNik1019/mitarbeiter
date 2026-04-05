
"""Session Factory."""

from typing import Final

from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from mitarbeiter.config.db import (
    db_connect_args,
    db_log_statements,
    db_url,
)

__all__ = ["Session", "engine"]

engine: Final = create_engine(
    db_url,
    connect_args=db_connect_args,
    echo=db_log_statements,
)
"""'Engine' für SQLAlchemy, erstellt DB-Verbindung und Sessions."""

logger.info("Engine fuer SQLAlchemy erzeugt")


Session = sessionmaker(bind=engine, autoflush=False)
"""Factory für Sessions, um generierte SQL-Anweisungen in Transaktionen abzusetzen."""

logger.info("Session-Factory fuer SQLAlchemy erzeugt")
