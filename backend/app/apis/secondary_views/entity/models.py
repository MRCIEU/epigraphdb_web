from enum import Enum
from typing import Any, List, Optional

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


EntitySearchNodeResponse = create_model_from_typeddict(EntitySearchNode)
EntityMetaNeighboursResponse = create_model_from_typeddict(
    EntityMetaNeighbours
)
EntityNeighbourResponse = create_model_from_typeddict(EntityNeighbour)
