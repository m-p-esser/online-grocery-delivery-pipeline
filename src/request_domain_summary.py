"""Python script to request Domain Summary Endpoint"""

import requests
from prefect import flow, get_run_logger, task

from etl import persist, request
from utils.config import DomainSummaryRequestConfig


@task(
    retries=3,
    retry_delay_seconds=10,
    name="Request Domain Summary Endpoint",
    description="Request the Domain Summary Serpstat API endpoint (https://serpstat.com/api/412-summarnij-otchet-po-domenu-v4-serpstatdomainproceduregetdomainsinfo/",
)
def request_domain_summary_endpoint(method: str, params: dict):
    """Request the Domain Summary Serpstat API endpoint"""

    logger = get_run_logger()

    response = request.request_serpstats_api(method, params)

    logger.info("INFO level log messages")
    logger.info(f"Requested API endpoint: {method}")
    logger.info(f"Using the following parameters: {params}")

    return response


@task
def parse_domain_summary_endpoint_response(response: requests.Response):
    """Parse the response from the Domain Summary Serpstat API endpoint"""

    logger = get_run_logger()

    response_json = request.parse_response(response)

    logger.info("INFO level log messages")
    logger.info("Parsed the following API Response:")
    logger.info(response_json)

    return response_json


@task
def save_domain_summary_endpoint_result(
    response_json: dict, save_path: str, save_location: str
):
    """Save the result from the Domain Summary Serpstat API endpoint"""

    logger = get_run_logger()

    persist.save_result(response_json, save_path, save_location)

    logger.info("INFO level log message")
    logger.info(f"Saved API response ({save_location}) here: {save_path}")


@flow
def domain_summary_endpoint_request_flow(config: DomainSummaryRequestConfig):
    """Flow to request the Domain Summary Serpstat API endpoint"""

    response = request_domain_summary_endpoint(config.method, config.params)
    result = parse_domain_summary_endpoint_response(response)
    save_domain_summary_endpoint_result(
        result, config.save_path, config.save_location
    )


if __name__ == "__main__":
    domain_summary_endpoint_request_flow(config=DomainSummaryRequestConfig())
