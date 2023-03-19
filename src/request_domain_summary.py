"""Python script to request Domain Summary Endpoint"""

import requests
from prefect import flow, task

from etl import request
from utils import config


@task(
    retries=3,
    retry_delay_seconds=10,
    name="Request Domain Summary Endpoint",
    description="Request the Domain Summary Serpstat API endpoint (https://serpstat.com/api/412-summarnij-otchet-po-domenu-v4-serpstatdomainproceduregetdomainsinfo/",
)
def request_domain_summary_endpoint(
    config: config.DomainSummaryRequestConfig(),
):
    """Request the Domain Summary Serpstat API endpoint"""

    method = config.method
    params = {"domains": config.domains, "database": config.database}
    response = request.request_serpstats_api(method, params)
    return response


@task
def parse_domain_summary_endpoint_response(response: requests.Response):
    """Parse the response from the Domain Summary Serpstat API endpoint"""

    response_json = request.parse_response(response)
    return response_json


@task
def save_domain_summary_endpoint_result(
    response_json: dict, save_location: str
):
    """Save the result from the Domain Summary Serpstat API endpoint"""
    request.save_result(response_json, save_location)


@flow
def domain_summary_endpoint_request_flow(
    config=config.DomainSummaryRequestConfig(),
    save_location=config.Location().data_raw_domain_summary,
):
    """Flow to request the Domain Summary Serpstat API endpoint"""

    response = request_domain_summary_endpoint(config)
    result = parse_domain_summary_endpoint_response(response)
    save_domain_summary_endpoint_result(result, save_location)


if __name__ == "__main__":
    domain_summary_endpoint_request_flow()
