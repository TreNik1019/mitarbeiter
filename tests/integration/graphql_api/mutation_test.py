"""Test für Mutationen mit GraphQL."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, graphql_url
from httpx import post
from pytest import mark


@mark.graphql
@mark.mutation
def test_create() -> None:
    """GraphQL-Post-Methode testen."""
    # arrange
    query: Final = {
        "query": """
            mutation {
                create(
                    mitarbeiterInput: {
                        nachname: "Testobj"
                        email: "test@firma.de"
                        position: ENTWICKLER
                        gehalt: "4500.00"
                        eintrittsdatum: "2020-02-20"
                        homepage: "https://test.firma.de"
                        geschlecht: WEIBLICH
                        werksausweis: {
                            status: AKTIV
                            guthaben: 36.0
                            ausstellungsdatum: "2023-04-24"
                        }
                        auftraege: [
                            {
                                bezeichnung: "Testauftrag"
                                auftragserteilung: "2025-01-01"
                                dauer: "2025-12-31"
                            }
                        ]
                        username: "testgql123"
                    }
                ) {
                    id
                }
            }
        """
    }

    # act
    response: Final = post(graphql_url, json=query, verify=ctx)

    # assert
    assert response is not None
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    assert isinstance(response_body["data"]["create"]["id"], int)
    assert response_body.get("errors") is None
