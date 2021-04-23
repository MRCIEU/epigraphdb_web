from typing import Any, List

from pydantic import BaseModel
from typing_extensions import TypedDict

from app.models.entities import AnnotatedMetaEntity, AnnotatedNodeId


class SearchEntity(TypedDict):
    id: AnnotatedNodeId
    name: str
    meta_node: AnnotatedMetaEntity


class SearchFull(TypedDict):
    results: List[SearchEntity]
    summary: Any


# NOTE: for some reasons pydantic fails to parse and convert typeddict
# in this case
class SearchEntityResponse(BaseModel):
    id: AnnotatedNodeId
    name: str
    meta_node: AnnotatedMetaEntity


class SearchFullResponse(BaseModel):
    results: List[SearchEntityResponse]
    summary: Any
