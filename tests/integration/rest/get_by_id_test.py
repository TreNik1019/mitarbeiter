# ruff: noqa: S101, D103

"""Tests für GET mit Pfadparameter für die ID."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, login, rest_url
from httpx import get
from pytest import mark


# in pyproject.toml bei der Table [tool.pytest.ini_options], Array "markers"
@mark.rest
@mark.get_request
@mark.parametrize("mitarbeiter_id", [30, 1, 20])
def test_get_by_id_admin(mitarbeiter_id: int) -> None:
    # vorbereiten
    token: Final = login()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    # ausführen
    response: Final = get(
        f"{rest_url}/{mitarbeiter_id}",
        headers=headers,
        verify=ctx,
    )

    # überprüfen
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    id_actual: Final = response_body.get("id")
    assert id_actual is not None
    assert id_actual == mitarbeiter_id


@mark.rest
@mark.get_request
@mark.parametrize("mitarbeiter_id", [0, 999999])
def test_get_by_id_not_found(mitarbeiter_id: int) -> None:
    # arrange
    token: Final = login()
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(
        f"{rest_url}/{mitarbeiter_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.NOT_FOUND


@mark.rest
@mark.get_request
def test_get_by_id_mitarbeiter() -> None:
    # arrange
    mitarbeiter_id: Final = 20
    token: Final = login(username="mueller")
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    # act
    response: Final = get(
        f"{rest_url}/{mitarbeiter_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    mitarbeiter_id_response: Final = response_body.get("id")
    assert mitarbeiter_id_response is not None
    assert mitarbeiter_id_response == mitarbeiter_id


@mark.rest
@mark.get_request
@mark.parametrize("mitarbeiter_id", [1, 30])
def test_get_by_id_not_allowed(mitarbeiter_id: int) -> None:

    token: Final = login(username="mueller")
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    response: Final = get(
        f"{rest_url}/{mitarbeiter_id}",
        headers=headers,
        verify=ctx,
    )

    assert response.status_code == HTTPStatus.FORBIDDEN


@mark.rest
@mark.get_request
@mark.parametrize("mitarbeiter_id", [0, 999999])
def test_get_by_id_not_allowed_not_found(mitarbeiter_id: int) -> None:

    token: Final = login(username="mueller")
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}

    response: Final = get(
        f"{rest_url}/{mitarbeiter_id}",
        headers=headers,
        verify=ctx,
    )

    assert response.status_code == HTTPStatus.FORBIDDEN


@mark.rest
@mark.get_request
@mark.parametrize("mitarbeiter_id", [30, 1, 20])
def test_get_by_id_ungueltiger_token(mitarbeiter_id: int) -> None:

    token: Final = login()
    assert token is not None
    headers = {"Authorization": f"Bearer {token}XXX"}

    response: Final = get(
        f"{rest_url}/{mitarbeiter_id}",
        headers=headers,
        verify=ctx,
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


@mark.rest
@mark.get_request
@mark.parametrize("mitarbeiter_id", [30, 1, 20])
def test_get_by_id_ohne_token(mitarbeiter_id: int) -> None:

    response: Final = get(f"{rest_url}/{mitarbeiter_id}", verify=ctx)

    assert response.status_code == HTTPStatus.UNAUTHORIZED


@mark.rest
@mark.get_request
@mark.parametrize("mitarbeiter_id,if_none_match", [(20, '"0"'), (30, '"0"')])
def test_get_by_id_etag(mitarbeiter_id: int, if_none_match: str) -> None:

    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
        "If-None-Match": if_none_match,
    }

    response: Final = get(
        f"{rest_url}/{mitarbeiter_id}",
        headers=headers,
        verify=ctx,
    )

    assert response.status_code == HTTPStatus.NOT_MODIFIED
    assert not response.text


@mark.rest
@mark.get_request
@mark.parametrize(
    "mitarbeiter_id,if_none_match", [(30, 'xxx"'), (1, "xxx"), (20, "xxx")]
)
def test_get_by_id_etag_invalid(mitarbeiter_id: int, if_none_match: str) -> None:
    # arrange
    token: Final = login()
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}",
        "If-None-Match": if_none_match,
    }

    # act
    response: Final = get(
        f"{rest_url}/{mitarbeiter_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    id_actual: Final = response_body.get("id")
    assert id_actual is not None
    assert id_actual == mitarbeiter_id
