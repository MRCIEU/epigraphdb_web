from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class NeighbourItemResponse(BaseModel):
    meta_node: str
    meta_rel: str
    node_data: Dict[str, Any]


class NeighbourResultsResponse(BaseModel):
    meta_node: str
    id: str
    neighbour: List[NeighbourItemResponse]


class NodeInfoResultsResponse(BaseModel):
    node: Dict[str, Any]


class NeighbourGraphDataResponse(BaseModel):
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
    nodes_3d: List[Dict[str, Any]]
    edges_3d: List[Dict[str, Any]]
    option: Dict[str, Any]


class LinkedResourceResponse(BaseModel):
    name: Optional[str]
    url: Optional[str]
    logo: Optional[str]


class NodeInfoResponse(BaseModel):
    results: List[NodeInfoResultsResponse]
    meta_node: str
    id: Optional[str]
    name: Optional[str]
    # neighbour results and neighbour graph are only non-empty
    # when searched by id rather by name
    neighbour_results: Optional[NeighbourResultsResponse]
    neighbour_graph_data: Optional[NeighbourGraphDataResponse]
    doc_url: str
    linked_resource: LinkedResourceResponse


class ExploreResponse(BaseModel):
    node_info: NodeInfoResponse
    empty_results: bool
