from dataclasses import dataclass
from enum import Enum
from typing import List

from app.funcs.network_graph import NetworkEdgeSchema, NetworkNodeSchema


class GalleryQueryType(str, Enum):
    cypher = "cypher"
    api = "api"


@dataclass
class GallerySchema:
    nodes: List[NetworkNodeSchema]
    edges: List[NetworkEdgeSchema]


@dataclass
class GalleryGraph:
    name: str
    title: str
    description: str
    query: str
    query_type: GalleryQueryType
    schema: GallerySchema
