from typing import List, Optional

from fastapi import APIRouter, Query

from app.models.meta_graph import EpigraphdbMetaNodeForSearch
from app.utils.database import es_client

from . import models
from .functions import (
    annotate_search_results,
    get_index_name,
    index_node_info,
    query_node_info,
    summarise_results,
)

router = APIRouter()


@router.get(
    "/search/quick/node",
    response_model=List[Optional[models.SearchEntityResponse]],
)
def get_search_quick(
    meta_node: Optional[EpigraphdbMetaNodeForSearch] = None,
    q: str = Query(..., min_length=3),
    size: int = 100,
) -> List[Optional[models.SearchEntity]]:
    if meta_node is None:
        search_results = query_node_info(query=q, meta_node=None, size=size)
    else:
        index_name = get_index_name(meta_node.value)
        if not es_client.indices.exists(index=index_name):
            return []
        else:
            search_results = query_node_info(
                query=q, meta_node=meta_node.value, size=size
            )
    res = annotate_search_results(search_results)
    return res


@router.get(
    "/search/full/node",
    response_model=Optional[models.SearchFullResponse],
)
def get_search_full(
    meta_node: Optional[EpigraphdbMetaNodeForSearch] = None,
    q: str = Query(..., min_length=3),
    size: int = 500,
) -> Optional[models.SearchFull]:
    if meta_node is None:
        search_results = query_node_info(query=q, meta_node=None, size=size)
    else:
        index_name = get_index_name(meta_node.value)
        if not es_client.indices.exists(index=index_name):
            search_results = []
        else:
            search_results = query_node_info(
                query=q, meta_node=meta_node.value, size=size
            )
    summary = None
    if len(search_results) == 0:
        return None
    else:
        summary = summarise_results(search_results)
        annotated_results = annotate_search_results(search_results)
        res = {"results": annotated_results, "summary": summary}
        return res


@router.get("/search/es/node/{meta_node}/index", response_model=bool)
def get_index_node(
    meta_node: EpigraphdbMetaNodeForSearch, overwrite: bool = False
) -> bool:
    index_name = get_index_name(meta_node.value)
    if not es_client.indices.exists(index=index_name) or overwrite:
        return index_node_info(meta_node=meta_node.value, overwrite=overwrite)
    else:
        return True


@router.get("/search/es/index", response_model=bool)
def get_index_all(overwrite: bool = False):
    "Index elasticsearch indices."
    meta_nodes = [item for item in EpigraphdbMetaNodeForSearch]
    index_res = [
        get_index_node(meta_node=meta_node, overwrite=overwrite)
        for meta_node in meta_nodes
    ]
    return sum(index_res) == len(meta_nodes)
