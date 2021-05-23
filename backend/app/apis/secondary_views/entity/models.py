from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import create_model_from_typeddict
from typing_extensions import TypedDict

from app.apis.util_routes.search.models import SearchEntity
from app.models.entities import (
    AnnotatedMetaEntity,
    AnnotatedNodeId,
    AnnotatedProperty,
)


class LinkedResource(TypedDict):
    name: str
    url: str
    logo: str


class EntitySearchNodeItem(TypedDict):
    key: str
    value: Any
    annotation: AnnotatedProperty


class EntitySearchNode(TypedDict):
    meta_node: AnnotatedMetaEntity
    entity_id: str
    entity_name: str
    entity_source: List[str]
    full_data: List[EntitySearchNodeItem]
    linked_resource: Optional[LinkedResource]


class EntityMetaNeighbourItem(TypedDict):
    meta_node: AnnotatedMetaEntity
    meta_rel: AnnotatedMetaEntity
    meta_node_type: str
    count: int


class EntityResource(TypedDict):
    key: str
    name: str
    label: str
    url: str
    queriable: bool = False


class EntityResources(TypedDict):
    api: List[EntityResource]
    web: List[EntityResource]
    rpkg: List[EntityResource]


class EntityMetaNeighbours(TypedDict):
    meta_node_list: List[str]
    meta_rel_list: List[str]
    entity_resources: EntityResources
    full_data: List[EntityMetaNeighbourItem]


class EntityNeighbour(TypedDict):
    meta_node: AnnotatedMetaEntity
    meta_rel: AnnotatedMetaEntity
    node_id: AnnotatedNodeId
    node_name: str
    node_type: str


class EntitySimilarResults(TypedDict):
    summary: Any
    results: List[SearchEntity]


class EntityNodeType(str, Enum):
    source = "source"
    target = "target"


class MetaNodeData(TypedDict):
    url: str
    id_prop: str
    name_prop: str
    props: List[Dict[str, Any]]
    statistics: List[Dict[str, Any]]
    neighbours: List[EntityMetaNeighbourItem]
    linked_resource: Optional[LinkedResource]


class MetaRelData(TypedDict):
    url: str
    source_meta_node: AnnotatedMetaEntity
    target_meta_node: AnnotatedMetaEntity
    props: Optional[List[Dict[str, Any]]]
    statistics: List[Dict[str, Any]]
    linked_resource: Optional[LinkedResource]


class MetaNodeEntitySearchItem(TypedDict):
    node_id: AnnotatedNodeId
    node_name: str
    node_data: Dict[str, Any]


class MetaRelEntitySearchItem(TypedDict):
    source_node_info: Dict[str, Any]
    target_node_info: Dict[str, Any]
    source_data: List[Dict[str, Any]]
    target_data: List[Dict[str, Any]]
    rel_data: List[Dict[str, Any]]


class MetaNodeEntitySearch(TypedDict):
    items: Optional[List[MetaNodeEntitySearchItem]]


class MetaRelEntitySearch(TypedDict):
    rel_cols: Optional[List[str]]
    items: Optional[List[MetaRelEntitySearchItem]]


EntitySearchNodeResponse = create_model_from_typeddict(EntitySearchNode)
EntityMetaNeighboursResponse = create_model_from_typeddict(
    EntityMetaNeighbours
)
EntityNeighbourResponse = create_model_from_typeddict(EntityNeighbour)
MetaNodeDataResponse = create_model_from_typeddict(MetaNodeData)
MetaRelDataResponse = create_model_from_typeddict(MetaRelData)
MetaNodeEntitySearchResponse = create_model_from_typeddict(
    MetaNodeEntitySearch
)
MetaRelEntitySearchResponse = create_model_from_typeddict(MetaRelEntitySearch)
