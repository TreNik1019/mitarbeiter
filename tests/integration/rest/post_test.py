# ruff: noqa: S101, D103

"""Tests für POST."""

from http import HTTPStatus
from re import search
from typing import Final

from common_test import ctx, rest_url
from httpx import post
from pytest import mark

token: str | None


@mark.rest
@mark.post_request
def test_post() -> None:
    # arrange
    neuer_mitarbeiter: Final = {
        "nachname": "Mustermann",
        "email": "testrest@rest.de",
        "position": "TE",
        "gehalt": 5000.0,
        "eintrittsdatum": "2026-02-01",
        "homepage": "https://rest.de",
        "geschlecht": "W",
        "werksausweis": {
            "status": "G",
            "ausstellungsdatum": "2026-02-01",
            "guthaben": 15.0,
        },
        "auftraege": [
            {
                "bezeichnung": "Restprojekt",
                "auftragserteilung": "2026-02-01",
                "dauer": "2026-02-28",
            }
        ],
        "username": "testrest",
    }
    headers = {"Content-Type": "application/json"}

    # act
    response: Final = post(
        rest_url,
        json=neuer_mitarbeiter,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.CREATED
    location: Final = response.headers.get("Location")
    assert location is not None
    int_pattern: Final = "[1-9][0-9]*$"
    assert search(int_pattern, location) is not None
    assert not response.text


@mark.rest
@mark.post_request
def test_post_invalid() -> None:
    # arrange
    neuer_mitarbeiter_invalid: Final = {
        "nachname": "falscher_nachname",
        "email": "falsche_email@com",
        "position": "INVALID",
        "gehalt": 5000.0,
        "eintrittsdatum": "2026-02-01",
        "homepage": "keine-url",
        "geschlecht": "W",
        "werksausweis": {
            "status": "X",
            "ausstellungsdatum": "2026-02-01",
            "guthaben": 15.0,
        },
        "auftraege": [
            {
                "bezeichnung": "Restprojekt",
                "auftragserteilung": "2026-02-01",
                "dauer": "2026-02-28",
            }
        ],
        "username": "testrestinvalid",
    }
    headers = {"Content-Type": "application/json"}

    # act
    response: Final = post(
        rest_url,
        json=neuer_mitarbeiter_invalid,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    body = response.text
    assert "nachname" in body
    assert "email" in body
    assert "position" in body
    assert "homepage" in body
    assert "status" in body


@mark.rest
@mark.post_request
def test_post_email_exists() -> None:
    # arrange
    email_exists: Final = "mueller@firma.de"
    neuer_mitarbeiter: Final = {
        "nachname": "Nachnamerest",
        "email": email_exists,
        "position": "TE",
        "gehalt": 5000.0,
        "eintrittsdatum": "2026-02-01",
        "homepage": "https://rest.de",
        "geschlecht": "W",
        "werksausweis": {
            "status": "G",
            "ausstellungsdatum": "2026-02-01",
            "guthaben": 15.0,
        },
        "auftraege": [
            {
                "bezeichnung": "Restprojekt",
                "auftragserteilung": "2026-02-01",
                "dauer": "2026-02-28",
            }
        ],
        "username": "emailexists",
    }
    headers = {"Content-Type": "application/json"}

    # act
    response: Final = post(
        rest_url,
        json=neuer_mitarbeiter,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert email_exists in response.text


@mark.rest
@mark.post_request
def test_post_invalid_json() -> None:
    # arrange
    json_invalid: Final = '{"nachname" "Nachname"}'
    headers = {"Content-Type": "application/json"}

    # act
    response: Final = post(
        rest_url,
        json=json_invalid,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert "should be a valid dictionary" in response.text
