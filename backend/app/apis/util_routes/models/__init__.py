from typing import List

from fastapi import APIRouter

from app.models.meta_graph import (
    EpigraphdbMetaNodeForSearch,
    EpigraphdbMetaNodeNonCodeName,
)
from epigraphdb_common_utils.epigraphdb_schema import (
    meta_nodes_dict,
    meta_rels_dict,
)

router = APIRouter()


@router.get("/models/epigraphdb-meta-nodes", response_model=List[str])
def get_epigraphdb_meta_nodes() -> List[str]:
    meta_nodes = [_ for _ in meta_nodes_dict.keys()]
    return meta_nodes


@router.get("/models/epigraphdb-meta-rels", response_model=List[str])
def get_epigraphdb_meta_rels() -> List[str]:
    meta_rels = [_ for _ in meta_rels_dict.keys()]
    return meta_rels


@router.get("/models/meta-nodes/non-code-name", response_model=List[str])
def get_meta_nodes_non_code_name():
    return [_.value for _ in EpigraphdbMetaNodeNonCodeName]


@router.get("/models/meta-nodes/for-search", response_model=List[str])
def get_meta_nodes_for_search():
    return [_.value for _ in EpigraphdbMetaNodeForSearch]
