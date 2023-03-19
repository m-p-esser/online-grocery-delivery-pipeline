""" Module to create a BigQuery table from Schema"""

import hydra
from google.cloud import bigquery
from prefect_gcp.credentials import GcpCredentials


# Converts schema dictionary to BigQuery's expected format for job_config.schema
def format_schema(schema):
    formatted_schema = []
    for row in schema:
        formatted_schema.append(
            bigquery.SchemaField(row["name"], row["type"], row["mode"])
        )
    return formatted_schema


@hydra.main(config_path="conf/raw", config_name="domain_summary_schema")
def create_table(config):

    # Load Credentials and Config
    gcp_credentials = GcpCredentials.load("gcp-credentials")
    project_id = gcp_credentials.project
    dataset_id = config.dataset_id
    table_name = config.table_name

    # Init Client
    client = bigquery.Client(project=gcp_credentials.project)

    # Prepare Schema from YAML format to BigQuery format
    schema = format_schema(config.schema)

    # Create Table
    table_id = f"{project_id}.{dataset_id}.{table_name}"
    table = bigquery.Table(table_id, schema)
    table = client.create_table(table)  # Make an API request
    print(f"Created table {project_id}.{dataset_id}.{table_name}")


if __name__ == "__main__":
    create_table()
