""" Tests for request module """

import pytest

from src.etl.request import parse_response, request_serpstats_api, save_result


@pytest.fixture()
def sucessful_request_serpstats_api():
    response = request_serpstats_api(
        method="SerpstatDomainProcedure.getDomainsInfo",
        params={"domains": ["shop.rewe.de"], "database": "g_de"},
    )
    return response


def test_request_is_sucessful(sucessful_request_serpstats_api):
    """Test if the response is sucessful (200)"""

    response = sucessful_request_serpstats_api

    assert response.status_code == 200


def test_parse_response(sucessful_request_serpstats_api):
    """Test if the response is parsed correctly"""

    response = sucessful_request_serpstats_api
    response_json = parse_response(response)

    assert isinstance(response_json, dict)


def test_reponse_contains_correct_data(sucessful_request_serpstats_api):
    """Test if the response contains the correct data"""

    response = sucessful_request_serpstats_api

    assert response.json()["result"]["data"][0]["domain"] == "shop.rewe.de"
