""" Create Pydantic Configuration models """

from typing import Optional

from pydantic import BaseModel


class DomainSummaryRequestParams(BaseModel):
    """Parameters for requesting the Domain Summary Serpstat API endpoint"""

    domains: list[str] = ["shop.rewe.de", "www.edeka24.de"]
    database: str = "g_de"


class DomainSummaryRequestConfig(BaseModel):
    """Configuration for requesting the Domain Summary Serpstat API endpoint"""

    method: str = "SerpstatDomainProcedure.getDomainsInfo"
    params: dict = dict(DomainSummaryRequestParams())
    save_path: str = "data/raw/domain_summary.json"
    save_location: str = "local"
