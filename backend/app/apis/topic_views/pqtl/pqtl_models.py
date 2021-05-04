from enum import Enum
from typing import Any, Dict, List, Union

from pydantic import BaseModel


class PQTLSearchType(str, Enum):
    exposures = "exposures"
    outcomes = "outcomes"


class PQTLSearchGroup(str, Enum):
    proteins = "proteins"
    traits = "traits"


class PQTLMethod(str, Enum):
    # basic summary
    simple = "simple"
    # mr results
    mrres = "mrres"
    # single snp mr
    sglmr = "sglmr"
    # snp information
    inst = "inst"
    # sensitivity analysis
    sense = "sense"


class PQTLNetworkPlotResponse(BaseModel):
    nodes: List[Dict[str, Any]]
    links: List[Dict[str, Any]]


class PQTLHighchartResponse(BaseModel):
    topres: List[Dict[str, Any]]
    otherres: List[Dict[str, Any]]


class PQTLTableResponse(BaseModel):
    table_fields: List[Dict[str, Any]]
    table_items: List[Dict[str, Any]]
    table_options: Any


class PQTLResponse(BaseModel):
    table_output: PQTLTableResponse
    plot_output: Union[PQTLNetworkPlotResponse, PQTLHighchartResponse]
    no_results: bool
    hierarchy: bool
    search_flag: str


class PQTLListTableResponse(BaseModel):
    table_titles: List[Dict[str, str]]
    table_data: List[Dict[str, Any]]


class PQTLOutcome(BaseModel):
    mrbase_id: str
    label: str
