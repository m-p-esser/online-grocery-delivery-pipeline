"""Python module related to persist data"""

import json

from prefect import get_run_logger
from prefect_gcp.bigquery import bigquery_load_cloud_storage
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp.credentials import GcpCredentials


def save_result_as_file(
    response_json: dict, save_path: str, save_location: str = "local"
):
    """Save the response_json to a file

    Parameters
    ----------
    response_json : dict
        The response_json to save
    save_path : str
        The location to save the response_json
    save_location : str, optional
        The location to store the response_json, by default "local"
    """

    allowed_save_locations = ["local", "gcs"]
    if save_location not in allowed_save_locations:
        raise ValueError(
            "save_location must be one of the following values: {}".format(
                allowed_save_locations
            )
        )

    if save_location == "local":
        with open(save_path, "w") as f:
            json.dump(response_json, f, indent=4)

    if save_location == "gcs":
        gcs_bucket = GcsBucket.load("gcs-bucket")
        with open(save_path, "rb") as f:
            gcs_bucket.upload_from_file_object(f, save_path)


def transfer_data_from_gcs_to_bigquery(
    dataset_id: str, table_name: str, gcs_uri: str
):
    """Load data from file stored in Google Cloud Storage (GCS) and store it in Google BigQuery Table

    Parameters
    ----------
    dataset_id : str
        The name of the dataset
    table_name : str
        The name of the table
    gcs_uri : str
        The URI of the file in GCS
    """

    logger = get_run_logger()

    # Load GCP credentials from the context
    gcp_credentials = GcpCredentials.load("gcp-credentials")

    # Load data from GCS to BigQuery
    result = bigquery_load_cloud_storage(
        dataset=dataset_id,
        table=table_name,
        uri=gcs_uri,
        gcp_credentials=gcp_credentials,
    )

    logger.info("INFO level log message")
    logger.info(
        f"Inserted API response to BigQuery here: {dataset_id}.{table_name}"
    )

    return result
