"""Tests für Queries mit GraphQL."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, graphql_url, login_graphql
from httpx import post
from pytest import mark

GRAPHQL_PATH: Final = "/graphql"


@mark.graphql
@mark.query
def test_query_id() -> None:
    """Test: Mitarbeiter mit ID(10) vorhanden?."""
    # arrange
    token: Final = login_graphql()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    query: Final = {
        "query": """
            {
                mitarbeiter(mitarbeiterId: "60") {
                    version
                    nachname
                    email
                    position
                    gehalt
                    eintrittsdatum
                    geschlecht
                    homepage
                    werksausweis {
                        status
                        guthaben
                        ausstellungsdatum
                    }
                    username
                }
            }
        """,
    }

    # act
    response: Final = post(graphql_url, json=query, headers=headers, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    data: Final = response_body["data"]
    assert data is not None
    mitarbeiter: Final = data["mitarbeiter"]
    assert isinstance(mitarbeiter, dict)
    assert response_body.get("errors") is None


@mark.graphql
@mark.query
def test_query_email() -> None:
    """Test: Mitarbeiter mit Email("mueller@firma.de") vorhanden?."""
    # arrange
    token: Final = login_graphql()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    query: Final = {
        "query": """
            {
                mmitarbeiter(suchparameter: {email: "mueller@firma.de"}) {
                    id
                    version
                    nachname
                    email
                    position
                    gehalt
                    eintrittsdatum
                    homepage
                    geschlecht
                    werksausweis {
                        status
                        guthaben
                        ausstellungsdatum
                    }
                    username
                }
            }
        """,
    }

    # act
    response: Final = post(graphql_url, json=query, headers=headers, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    mitarbeiter: Final = response_body["data"]["mmitarbeiter"]
    assert isinstance(mitarbeiter, list)
    assert len(mitarbeiter) > 0
    assert response_body.get("errors") is None


@mark.graphql
@mark.query
def test_query_nachname() -> None:
    """Test: Mitarbeiter mit Nachnamen(Wagner) vorhanden ?."""
    # arrange
    token: Final = login_graphql()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}

    query: Final = {
        "query": """
            {
                mmitarbeiter(suchparameter: {nachname: "Wagner"})  {
                    id
                    version
                    nachname
                    email
                    position
                    gehalt
                    eintrittsdatum
                    homepage
                    geschlecht
                    werksausweis {
                        status
                        guthaben
                        ausstellungsdatum
                    }
                    username
                }
            }
        """,
    }

    # act
    response: Final = post(graphql_url, json=query, headers=headers, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    mitarbeiter: Final = response_body["data"]["mmitarbeiter"]
    assert isinstance(mitarbeiter, list)
    assert len(mitarbeiter) > 0
    assert response_body.get("errors") is None
