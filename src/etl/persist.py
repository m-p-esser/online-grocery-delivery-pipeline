"""Python module related to persist data"""

import json
from io import BytesIO

from prefect_gcp.cloud_storage import GcsBucket


def save_result(
    response_json: dict, save_location: str, store_location: str = "local"
):
    """Save the response_json to a file

    Parameters
    ----------
    response_json : dict
        The response_json to save
    save_location : str
        The location to save the response_json
    store_location : str, optional
        The location to store the response_json, by default "local"
    """

    allowed_store_locations = ["local", "gcs"]
    if store_location not in allowed_store_locations:
        raise ValueError(
            "store_location must be one of the following values: {}".format(
                allowed_store_locations
            )
        )

    if store_location == "local":
        with open(save_location, "w") as f:
            json.dump(response_json, f, indent=4)

    if store_location == "gcs":
        gcs_bucket = GcsBucket.load("gcs-bucket")
        with open(save_location, "rb") as f:
            gcs_bucket.upload_from_file_object(f, save_location)
