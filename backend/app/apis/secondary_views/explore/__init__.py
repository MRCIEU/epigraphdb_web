from typing import Optional

from fastapi import APIRouter

from app.models.meta_graph import EpigraphdbMetaNode

from .models import ExploreResponse
from .node_match import node_match
from .path_match import path_match

router = APIRouter()


@router.get("/explore/search/node", response_model=ExploreResponse)
def get_explore_search_node(
    meta_node: EpigraphdbMetaNode,
    id: Optional[str] = None,
    name: Optional[str] = None,
):
    res = node_match(meta_node=meta_node.value, id=id, name=name)
    return res


@router.get("/explore/search/path")
def get_explore_search_path(
    meta_node_source: EpigraphdbMetaNode,
    id_source: str,
    meta_node_target: EpigraphdbMetaNode,
    id_target: str,
    max_path_length: int = 3,
    limit: int = 100,
):
    res = path_match(
        meta_node_source=meta_node_source.value,
        meta_node_target=meta_node_target.value,
        id_source=id_source,
        id_target=id_target,
        max_path_length=max_path_length,
        limit=limit,
    )
    return res
