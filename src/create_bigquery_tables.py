""" Module to create a BigQuery table from Schema"""

from google.cloud import bigquery
from prefect_gcp.credentials import GcpCredentials

from utils.data_models import BigQuerySchema, DomainSummaryBigQuerySchema


def create_bigquery_dataset(dataset_id: str):
    """
    Creates a BigQuery Dataset.

    Args:
        dataset_id: The name of the dataset to be created.
    """
    # Load Credentials and Config
    gcp_credentials = GcpCredentials.load("gcp-credentials")
    project_id = gcp_credentials.project

    # Init Client
    client = bigquery.Client(project=gcp_credentials.project)

    # Construct a full Dataset object to send to the API
    dataset_ref = f"{project_id}.{dataset_id}"
    dataset = bigquery.Dataset(dataset_ref)

    # Make an API request to create dataset
    dataset = client.create_dataset(dataset, exists_ok=True)
    print(f"Created dataset {client.project}.{dataset.dataset_id}")


def create_bigquery_table(biqquery_schema: BigQuerySchema):
    """
    Creates a BigQuery Table.

    Args:
        dataset_id: BiqQuerySchema Data Model.
    """
    # Load Credentials and Config
    gcp_credentials = GcpCredentials.load("gcp-credentials")
    project_id = gcp_credentials.project

    # Init Client
    client = bigquery.Client(project=gcp_credentials.project)

    # Construct a full Table object to send to the API
    dataset_id = biqquery_schema.dataset_id
    table_name = biqquery_schema.table_name
    table_id = f"{project_id}.{dataset_id}.{table_name}"
    table = bigquery.Table(table_id, biqquery_schema.schema_definition)

    # Make an API request to create table
    client.create_dataset(dataset_id, exists_ok=True)
    table = client.create_table(table)
    print(f"Created table {project_id}.{dataset_id}.{table_name}")


if __name__ == "__main__":

    # Create multiple dataset(s) and tables
    domain_summary_bigquery_schema = DomainSummaryBigQuerySchema()
    create_bigquery_dataset(domain_summary_bigquery_schema.dataset_id)
    create_bigquery_table(domain_summary_bigquery_schema)
