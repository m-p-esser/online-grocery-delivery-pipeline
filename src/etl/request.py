"""Python script to request API"""

import json

import requests
from prefect.blocks.system import Secret


def request_serpstats_api(method: str, params: dict):
    """
    Request the API

    Parameters
    ----------
    method : str
        The API method to use
    params : dict
        The parameters to pass to the API
    """

    try:

        api_token = Secret.load("serp-stats-api-key").get()
        api_url_pattern = "https://api.serpstat.com/v{version}?token={token}"

        api_url = api_url_pattern.format(version=4, token=api_token)

        data = {
            "id": "1",
            "method": method,
            "params": {"domains": params["domains"], "se": params["database"]},
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


def parse_response(response: requests.Response):
    """Extract data from response and return as dict

    Parameters
    ----------
    response : requests.Response
    """

    response_json = response.json()
    return response_json


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
