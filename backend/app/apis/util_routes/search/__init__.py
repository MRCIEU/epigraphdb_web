from typing import List, Optional

from fastapi import APIRouter, Query

from app.utils.database import es_client

from .functions import get_index_name, index_node_info, query_node_info
from .models import EpigraphdbMetaNode, SearchEntityResponse

router = APIRouter()


@router.get(
    "/search/global/node/{meta_node}",
    response_model=List[Optional[SearchEntityResponse]],
)
def get_search_node(
    meta_node: EpigraphdbMetaNode,
    q: str = Query(..., min_length=3),
    size: int = 40,
):
    index_name = get_index_name(meta_node.value)
    if not es_client.indices.exists(index=index_name):
        res = []
    else:
        res = query_node_info(query=q, meta_node=meta_node.value)
    return res


@router.get("/search/global/node/{meta_node}/index", response_model=bool)
def get_index_node(
    meta_node: EpigraphdbMetaNode, overwrite: bool = False
) -> bool:
    index_name = get_index_name(meta_node.value)
    if not es_client.indices.exists(index=index_name) or overwrite:
        return index_node_info(meta_node=meta_node.value, overwrite=overwrite)
    else:
        return True


@router.get("/search/global/index", response_model=bool)
def get_index_all(overwrite: bool = False):
    meta_nodes = [item for item in EpigraphdbMetaNode]
    index_res = [
        get_index_node(meta_node=meta_node, overwrite=overwrite)
        for meta_node in meta_nodes
    ]
    return sum(index_res) == len(meta_nodes)
