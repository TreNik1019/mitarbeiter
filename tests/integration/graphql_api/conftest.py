"""Fixture für pytest: Neuladen der Datenbank."""

from common_test import check_readiness, db_populate, keycloak_populate
from pytest import fixture

session_scope = "session"


@fixture(scope=session_scope, autouse=True)
def check_readiness_per_session() -> None:
    """Check, ob der Server bereit für Anfragen ist."""
    check_readiness()
    print("Appserver ist bereit.")


@fixture(scope=session_scope, autouse=True)
def populate_per_session() -> None:
    """Fixture, um die Datenbank und Keycloak neu zu laden."""
    db_populate()
    print("DB ist neu geladen.")
    keycloak_populate()
    print("Keycloak ist neu geladen")
