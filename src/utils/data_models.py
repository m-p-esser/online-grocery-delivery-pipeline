""" Create Pydantic Data models """

from google.cloud import bigquery
from pydantic import BaseModel


# Base Data Model for BigQuery Schema
class BigQuerySchema(BaseModel):
    dataset_id: str
    table_name: str
    schema_definition: list


class DomainSummaryBigQuerySchema(BigQuerySchema):
    dataset_id = "raw_online_grocery_delivery"
    table_name = "domain_summary"
    schema_definition = [
        bigquery.SchemaField("id", "STRING", "REQUIRED"),
        bigquery.SchemaField("data", "JSON", "REQUIRED"),
        bigquery.SchemaField("summary_info", "JSON", "REQUIRED"),
    ]
