"""Python module related to persist data"""

import json
from io import BytesIO

from prefect_gcp.cloud_storage import GcsBucket


def save_result(
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
