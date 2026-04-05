"""Exceptions."""

from collections.abc import Mapping

__all__ = [
    "EmailExistsError",
    "ForbiddenError",
    "NotFoundError",
    "UsernameExistsError",
    "VersionOutdatedError",
]


class EmailExistsError(Exception):
    """Exception, wenn email bereits existiert."""

    def __init__(self, email: str) -> None:
        """Initialisierung von EmailExistsError mit der Emailadresse.

        :param email: Bereits existierende Emailadresse
        """
        super().__init__(f"Existierende Email: {email}")
        self.email = email


class UsernameExistsError(Exception):
    """Exception, wenn der username schon existiert."""

    def __init__(self, username: str) -> None:
        """Initialisierung von UsernameExistsError mit dem Benutzernamen.

        :param username: Bereits existierender Benutzername
        """
        super().__init__(f"Existierender Benutzername: {username}")
        self.username = username


class ForbiddenError(Exception):
    """Exception, falls es der Zugriff nicht erlaubt ist."""


class NotFoundError(Exception):
    """Mitarbeiter nicht gefunden."""

    def __init__(
        self,
        mitarbeiter_id: int | None = None,
        suchparameter: Mapping[str, str] | None = None,
    ) -> None:
        """'id' bzw schlüssel-wert paare zu denen nichts gefunden wurden."""
        super().__init__("Not Found")
        self.mitarbeiter_id = mitarbeiter_id
        self.suchparameter = suchparameter


class VersionOutdatedError(Exception):
    """Exception, falls die Versionsnummer beim Aktualisieren veraltet."""

    def __init__(self, version: int) -> None:
        """'versionsnummer# veraltet."""
        super().__init__(f"Veraltete Version: {version}")
        self.version = version
