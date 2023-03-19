"""Python script to request API"""

import json

import requests
from prefect import flow, task
from prefect.blocks.system import Secret

from config import Location, RequestConfig


@task
def request_api(method: str, domains: list, database: str):
    """
    Request the API

    Parameters
    ----------
    method : str
        The API method to use
    domains : list
        The domains for which data should be requested
    database : str
        The database from API to request the data from
    """

    try:

        api_token = Secret.load("serp-stats-api-key").get()
        api_url_pattern = "https://api.serpstat.com/v{version}?token={token}"

        api_url = api_url_pattern.format(version=4, token=api_token)

        data = {
            "id": "1",
            "method": method,
            "params": {"domains": domains, "se": database},
        }

        response = requests.post(api_url, json=data)

        response.raise_for_status()

    except requests.exceptions.HTTPError as error:
        print(f"HTTP error occurred: {error}")
    except requests.exceptions.ConnectionError as error:
        print(f"Connection error occurred: {error}")
    except requests.exceptions.Timeout as error:
        print(f"Timeout error occurred: {error}")
    except requests.exceptions.RequestException as error:
        print(f"An error occurred: {error}")

    return response


@task
def parse_response(response: requests.Response):
    """Extract data from response

    Parameters
    ----------
    response : requests.Response
    """

    response_json = response.json()
    return response_json


@task
def save_result(response_json: dict, save_location: str):
    """Save the response_json to a file

    Parameters
    ----------
    response_json : dict
        The response_json to save
    save_location : str
        The location to save the response_json
    """
    with open(save_location, "w") as f:
        json.dump(response_json, f, indent=4)


@flow
def request_api_flow(
    config: RequestConfig = RequestConfig(), location: Location = Location()
):
    """Flow to request the API

    Parameters
    ----------
    location : Location
        The location of the data
    config : ProcessConfig
        The configuration of the process

    """
    response = request_api(config.method, config.domains, config.database)
    result = parse_response(response)
    save_result(result, location.data_raw_domain_summary)


if __name__ == "__main__":
    request_api_flow()
