# ruff: noqa: S101, D103

"""Tests für PUT."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, login, rest_url
from httpx import put
from pytest import mark

EMAIL_UPDATE: Final = "mueller@firma.de.put"
HOMEPAGE_UPDATE: Final = "https://www.acme.ch.put"


@mark.rest
@mark.put_request
def test_put() -> None:
    # arrange
    mitarbeiter_id: Final = 40
    if_match: Final = '"0"'
    geaenderter_mitarbeiter: Final = {
        "nachname": "Müllerput",
        "email": EMAIL_UPDATE,
        "position": "ENTWICKLER",
        "gehalt": 6000,
        "eintrittsdatum": "2025-01-02",
        "homepage": HOMEPAGE_UPDATE,
    }
    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
        "If-Match": if_match,
    }

    # act
    response: Final = put(
        f"{rest_url}/{mitarbeiter_id}",
        json=geaenderter_mitarbeiter,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert not response.text


@mark.rest
@mark.put_request
def test_put_invalid() -> None:
    # arrange
    mitarbeiter_id: Final = 40
    geaenderter_mitarbeiter_invalid: Final = {
        "nachname": "falscher_nachname_put",
        "email": "falsche_email_put@",
        "position": "ENTWICKLER",
        "gehalt": 6000,
        "eintrittsdatum": "2025-01-02",
        "homepage": "https://?!",
    }
    token: Final = login()
    assert token is not None
    headers = {
        "If-Match": '"0"',
        "Authorization": f"Bearer {token}",
    }

    # act
    response: Final = put(
        f"{rest_url}/{mitarbeiter_id}",
        json=geaenderter_mitarbeiter_invalid,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert "nachname" in response.text
    assert "email" in response.text
    assert "position" in response.text
    assert "homepage" in response.text


@mark.rest
@mark.put_request
def test_put_nicht_vorhanden() -> None:
    # arrange
    mitarbeiter_id: Final = 999999
    if_match: Final = '"0"'
    geaenderter_mitarbeiter: Final = {
        "nachname": "Müllerput",
        "email": EMAIL_UPDATE,
        "position": "ENTWICKLER",
        "gehalt": 6000,
        "eintrittsdatum": "2025-01-02",
        "homepage": HOMEPAGE_UPDATE,
    }
    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
        "If-Match": if_match,
    }

    # act
    response: Final = put(
        f"{rest_url}/{mitarbeiter_id}",
        json=geaenderter_mitarbeiter,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.NOT_FOUND


@mark.rest
@mark.put_request
def test_put_email_exists() -> None:
    # arrange
    mitarbeiter_id: Final = 40
    if_match: Final = '"1"'
    email_exists: Final = "mueller@firma.de"
    geaenderter_mitarbeiter: Final = {
        "nachname": "Müllerput",
        "email": email_exists,
        "position": "ENTWICKLER",
        "gehalt": 6000,
        "eintrittsdatum": "2025-01-02",
        "homepage": HOMEPAGE_UPDATE,
    }
    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
        "If-Match": if_match,
    }

    # act
    response: Final = put(
        f"{rest_url}/{mitarbeiter_id}",
        json=geaenderter_mitarbeiter,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert email_exists in response.text


@mark.rest
@mark.put_request
def test_put_ohne_versionsnr() -> None:
    # arrange
    mitarbeiter_id: Final = 40
    geaenderter_mitarbeiter: Final = {
        "nachname": "Müllerput",
        "email": EMAIL_UPDATE,
        "position": "ENTWICKLER",
        "gehalt": 6000,
        "eintrittsdatum": "2025-01-02",
        "homepage": HOMEPAGE_UPDATE,
    }
    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
    }

    # act
    response: Final = put(
        f"{rest_url}/{mitarbeiter_id}",
        json=geaenderter_mitarbeiter,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.PRECONDITION_REQUIRED


@mark.rest
@mark.put_request
def test_put_alte_versionsnr() -> None:
    # arrange
    mitarbeiter_id: Final = 40
    if_match: Final = '"-1"'
    geaenderter_mitarbeiter: Final = {
        "nachname": "Müllerput",
        "email": EMAIL_UPDATE,
        "position": "ENTWICKLER",
        "gehalt": 6000,
        "eintrittsdatum": "2025-01-02",
        "homepage": HOMEPAGE_UPDATE,
    }
    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
        "If-Match": if_match,
    }

    # act
    response: Final = put(
        f"{rest_url}/{mitarbeiter_id}",
        json=geaenderter_mitarbeiter,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.PRECONDITION_FAILED


@mark.rest
@mark.put_request
def test_put_ungueltige_versionsnr() -> None:
    # arrange
    mitarbeiter_id: Final = 40
    if_match: Final = '"xy"'
    geaenderter_mitarbeiter: Final = {
        "nachname": "Müllerput",
        "email": EMAIL_UPDATE,
        "position": "ENTWICKLER",
        "gehalt": 6000,
        "eintrittsdatum": "2025-01-02",
        "homepage": HOMEPAGE_UPDATE,
    }
    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
        "If-Match": if_match,
    }

    # act
    response: Final = put(
        f"{rest_url}/{mitarbeiter_id}",
        json=geaenderter_mitarbeiter,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.PRECONDITION_FAILED
    assert not response.text


@mark.rest
@mark.put_request
def test_put_versionsnr_ohne_quotes() -> None:
    # arrange
    mitarbeiter_id: Final = 40
    if_match: Final = "0"
    geaenderter_mitarbeiter: Final = {
        "nachname": "Müllerput",
        "email": EMAIL_UPDATE,
        "position": "ENTWICKLER",
        "gehalt": 6000,
        "eintrittsdatum": "2025-01-02",
        "homepage": HOMEPAGE_UPDATE,
    }
    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
        "If-Match": if_match,
    }

    # act
    response: Final = put(
        f"{rest_url}/{mitarbeiter_id}",
        json=geaenderter_mitarbeiter,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.PRECONDITION_FAILED
