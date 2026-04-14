"""Schema für GraphQL."""

from datetime import date
from decimal import Decimal

import strawberry

from mitarbeiter.entity import Ausweisstatus, Geschlecht, Position

__all__ = [
    "AuftragInput",
    "CreatePayload",
    "MitarbeiterInput",
    "Suchparameter",
    "WerksausweisInput",
]


@strawberry.input
class AuftragInput:
    """Input-Objekt für Auftrag."""

    bezeichnung: str
    """Bezeichnung des Auftrags."""

    auftragserteilung: date
    """Datum der Auftragserteilung."""

    dauer: date
    """Deadline des Auftrags."""


@strawberry.input
class WerksausweisInput:
    """Input-Objekt für Werksausweis."""

    status: Ausweisstatus
    """Status des Werksausweises."""

    ausstellungsdatum: date
    """Ausstellungsdatum des Werksausweises."""

    guthaben: float
    """Guthaben auf dem Werksausweis."""


@strawberry.input
class MitarbeiterInput:
    """Input-Objekt für Mitarbeiter."""

    nachname: str
    """Nachname des Mitarbeiters."""

    email: str
    """Emailadresse des Mitarbeiters."""

    position: Position
    """Position des Mitarbeiters im Unternehmen."""

    gehalt: Decimal
    """Monatliches Gehalt des Mitarbeiters."""

    eintrittsdatum: date
    """Eintrittsdatum des Mitarbeiters."""

    homepage: str
    """Homepage des Unternehmens."""

    geschlecht: Geschlecht
    """Geschlecht des Mitarbeiters."""

    werksausweis: WerksausweisInput
    """Werksausweis des Mitarbeiters."""

    auftraege: list[AuftragInput]
    """Auftraege des Mitarbeiters."""


@strawberry.input
class Suchparameter:
    """Input-Objekt für Suchparameter."""

    nachname: str | None = None
    """Nachname des Mitarbeiters."""

    email: str | None = None
    """Emailadresse des Mitarbeiters."""


@strawberry.type
class CreatePayload:
    """Payload für die Create-Mutation."""

    id: int
    """ID des neu erstellten Mitarbeiters."""


@strawberry.type
class LoginResult:
    """Resultat, wenn der Login erfolgreich war."""

    token: str
    """Token des eingeloggten Benutzers."""

    expiresIn: str  # noqa: N815    # NOSONAR
    """Gültigkeitetsdauer des Tokens in Sekunden."""

    roles: list[str]
    """Rollen des eingeloggten Benutzers."""
