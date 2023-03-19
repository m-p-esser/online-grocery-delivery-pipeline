""" Create Pydantic models """
from typing import Any, Dict, List

from pydantic import BaseModel, validator


class Location(BaseModel):
    """Specify the locations of inputs and outputs"""

    data_raw_domain_summary: str = "data/raw/domain_summary.json"
    # data_process: str = "data/processed/xy.pkl"
    # data_final: str = "data/final/predictions.pkl"
    # model: str = "models/svc.pkl"
    # input_notebook: str = "notebooks/analyze_results.ipynb"
    # output_notebook: str = "notebooks/results.ipynb"


class DomainSummaryRequestConfig(BaseModel):
    """Specify the parameters for requesting the Domain Summary Endpoint of the Serpstat API"""

    method: str = "SerpstatDomainProcedure.getDomainsInfo"
    domains: List[str] = ["shop.rewe.de", "www.edeka24.de"]
    database: str = "g_de"
