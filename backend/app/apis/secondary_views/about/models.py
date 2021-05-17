from typing import Any, Dict, List

from pydantic import create_model_from_typeddict
from typing_extensions import TypedDict

from app.models import network_graph_models


class SchemaInfoGraphData(TypedDict):
    nodes: List[network_graph_models.VisNode]
    edges: List[network_graph_models.VisEdge]
    nodes_3d: List[network_graph_models.VisNode3d]
    edges_3d: List[network_graph_models.VisEdge3d]
    option: Dict[str, Any]


class SchemaInfoInfo(TypedDict):
    nodes: Dict[str, Any]
    rels: Dict[str, Any]


class SchemaInfoData(TypedDict):
    graph: SchemaInfoGraphData
    info: SchemaInfoInfo


class SchemaMetricsMetaNode(TypedDict):
    node_name: str
    count: int


class SchemaMetricsMetaRel(TypedDict):
    relationshipType: str
    count: int


class SchemaMetricsMetaPath(TypedDict):
    from_node: str
    to_node: str
    rel: str
    count: int


class SchemaMetricsData(TypedDict):
    meta_node: Dict[str, SchemaMetricsMetaNode]
    meta_rel: Dict[str, SchemaMetricsMetaRel]
    meta_path: Dict[str, SchemaMetricsMetaPath]


AboutSchemaResponse = create_model_from_typeddict(SchemaInfoData)

AboutSchemaMetrics = create_model_from_typeddict(SchemaMetricsData)
