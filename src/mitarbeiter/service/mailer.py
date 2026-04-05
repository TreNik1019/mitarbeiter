"""Mail."""

from email.mime.text import MIMEText
from email.utils import make_msgid
from smtplib import SMTP, SMTPServerDisconnected
from socket import gaierror
from typing import Final
from uuid import uuid4

from loguru import logger

from mitarbeiter.config import (
    mail_enabled,
    mail_host,
    mail_port,
    mail_timeout,
)
from mitarbeiter.service.mitarbeiter_dto import MitarbeiterDTO

__all__ = ["send_mail"]


MAILSERVER: Final = mail_host
PORT: Final = mail_port
SENDER: Final = "Python Server <python.server@acme.com>"
RECEIVERS: Final = ["Buchhaltung <buchhaltung@acme.com>"]
TIMEOUT: Final = mail_timeout


def send_mail(mitarbeiter_dto: MitarbeiterDTO) -> None:
    """df-Funktion, um mail zu senden."""
    logger.debug("{}", mitarbeiter_dto)
    if not mail_enabled:
        logger.warning("send_mail: Der Mailserver ist deaktiviert")
        return

    # Body + Subject und mail-id
    msg: Final = MIMEText(
        f"Neuer Mitarbeiter: <b>{mitarbeiter_dto.nachname}</b> "
        f"({mitarbeiter_dto.position})"
    )

    msg["Subject"] = f"Neuer Mitarbeiter: ID={mitarbeiter_dto.id}"
    msg["Message-ID"] = make_msgid(idstring=str(uuid4()))

    try:
        logger.debug("mailserver={}, port={}", MAILSERVER, PORT)
        with SMTP(host=MAILSERVER, port=PORT, timeout=TIMEOUT) as smtp:
            smtp.sendmail(from_addr=SENDER, to_addrs=RECEIVERS, msg=msg.as_string())
            logger.debug("msg={}", msg)

    except ConnectionRefusedError:
        logger.warning("ConnectionRefusedError")

    except SMTPServerDisconnected:
        logger.warning("SMTPServerDisconnected")

    except gaierror:
        logger.warning("socket.gaierror: Laeuft der Mailserver im virtuellen Netzwerk?")
