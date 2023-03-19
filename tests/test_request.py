""" Tests for request module """

import pytest
from prefect import flow
from prefect.logging import disable_run_logger

from src.request import parse_response, request_api, save_result


def test_task_request_getDomainsInfo_api():
    """Test Requesting the getDomainsInfo API"""

    @flow
    def test_flow():
        return request_api(
            method="SerpstatDomainProcedure.getDomainsInfo",
            domains=["shop.rewe.de"],
            database="g_de",
        )

    response = test_flow()

    # Check if the response is valid
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert isinstance(response.json()["result"], dict)
    assert isinstance(response.json()["result"]["data"], list)
    assert len(response.json()["result"]["data"]) == 1
    assert response.json()["result"]["data"][0]["domain"] == "shop.rewe.de"
