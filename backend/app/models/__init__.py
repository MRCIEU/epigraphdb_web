from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel


class DiagramResponse(BaseModel):
    nodes: List[Any]
    edges: List[Any]
    option: Dict[str, Any]


class ResponseDataResponse(BaseModel):
    query: str
    results: List[Any]


class QueryDataResponse(BaseModel):
    cypher: str
    curl: str
    api_snippet: Optional[str]
    r_pkg_snippet: Optional[str]
    response_data: ResponseDataResponse
    empty_results: bool


class GraphDataResponse(BaseModel):
    nodes: List[Any]
    edges: List[Any]
    nodes_3d: List[Any]
    edges_3d: List[Any]
    option: Dict[str, Any]
    num_paths_total: int
    num_paths_displayed: int


class TableDataResponse(BaseModel):
    table_titles: List[Dict[str, Any]]
    table_data: List[Dict[str, Any]]


class TopicResponse(BaseModel):
    query_data: QueryDataResponse
    graph_data: Optional[GraphDataResponse]
    table_data: Optional[TableDataResponse]
    empty_results: bool


class TopicViewEndpoints(str, Enum):
    table = "table"
    network_plot = "network-plot"
    query = "query"
    query_diagram = "query-diagram"


class EpigraphdbGraphs(str, Enum):
    epigraphdb = "epigraphdb"
    pqtl = "pqtl"


class EpigraphdbGraphsExtended(str, Enum):
    epigraphdb = "epigraphdb"
    pqtl = "pqtl"
    custom = "custom"


class RequestMethods(str, Enum):
    get = "GET"
    post = "POST"
    put = "PUT"
    delete = "DELETE"


standard_endpoint_response = Union[
    None,
    TableDataResponse,
    GraphDataResponse,
    QueryDataResponse,
    DiagramResponse,
]
