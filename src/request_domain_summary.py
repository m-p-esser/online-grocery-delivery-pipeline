"""Flow and Tasks to request Domain Summary Endpoint"""

import requests
from prefect import flow, get_run_logger, task

from etl import persist, request
from utils.config import DomainSummaryRequestConfig
from utils.data_models import BigQuerySchema


@task(
    retries=3,
    retry_delay_seconds=10,
    name="Request Domain Summary Endpoint",
    description="Request the Domain Summary Serpstat API endpoint (https://serpstat.com/api/412-summarnij-otchet-po-domenu-v4-serpstatdomainproceduregetdomainsinfo/",
)
def request_domain_summary_endpoint(
    method: str, params: dict
) -> requests.Response:
    """Request the Domain Summary Serpstat API endpoint"""

    logger = get_run_logger()

    response = request.request_serpstats_api(method, params)

    logger.info("INFO level log messages")
    logger.info(f"Requested API endpoint: {method}")
    logger.info(f"Using the following parameters: {params}")

    return response


@task
def parse_domain_summary_endpoint_response(
    response: requests.Response,
) -> dict:
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
) -> None:
    """Save the result from the Domain Summary Serpstat API endpoint"""

    logger = get_run_logger()

    persist.save_result(response_json, save_path, save_location)

    logger.info("INFO level log message")
    logger.info(f"Saved API response ({save_location}) here: {save_path}")


@flow
def domain_summary_endpoint_request_flow(
    config: DomainSummaryRequestConfig, bigquery_schema: BigQuerySchema
):
    """Flow to request the Domain Summary Serpstat API endpoint and store the results"""

    response = request_domain_summary_endpoint(config.method, config.params)

    result = parse_domain_summary_endpoint_response(response)

    save_domain_summary_endpoint_result(
        result, config.save_path, config.save_location
    )

    records = list(result)
    persist.insert_rows_to_bigquery_table(
        records, bigquery_schema.dataset_id, bigquery_schema.table_name
    )


if __name__ == "__main__":
    domain_summary_endpoint_request_flow(
        config=DomainSummaryRequestConfig(),
        bigquery_schema=BigQuerySchema(
            dataset_id="raw_online_grocery_delivery",
            table_name="domain_summary",
        ),
    )
