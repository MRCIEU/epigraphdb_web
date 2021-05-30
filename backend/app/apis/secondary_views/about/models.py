from typing import Any, Dict, List

from pydantic import create_model_from_typeddict
from typing_extensions import TypedDict

from app.models import network_graph_models
from app.models.entities import AnnotatedMetaEntity


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


class SchemaMetricsMetaNodeAnnotated(TypedDict):
    node_name: AnnotatedMetaEntity
    count: int


class SchemaMetricsMetaRel(TypedDict):
    relationshipType: str
    count: int


class SchemaMetricsMetaRelAnnotated(TypedDict):
    relationshipType: AnnotatedMetaEntity
    count: int


class SchemaMetricsMetaPath(TypedDict):
    from_node: str
    to_node: str
    rel: str
    count: int


class SchemaMetricsMetaPathAnnotated(TypedDict):
    from_node: AnnotatedMetaEntity
    to_node: AnnotatedMetaEntity
    rel: AnnotatedMetaEntity
    count: int


class SchemaMetricsData(TypedDict):
    meta_node: List[SchemaMetricsMetaNodeAnnotated]
    meta_rel: List[SchemaMetricsMetaRelAnnotated]
    meta_path: List[SchemaMetricsMetaPathAnnotated]


AboutSchemaResponse = create_model_from_typeddict(SchemaInfoData)

AboutSchemaMetrics = create_model_from_typeddict(SchemaMetricsData)
