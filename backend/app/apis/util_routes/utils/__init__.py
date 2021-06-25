from typing import List, Optional

from fastapi import APIRouter

from app.utils.database import es_client, mongo_epigraphdb_web

router = APIRouter()


@router.get("/utils/cache/drop", response_model=bool)
def get_utils_cache_drop(
    collection_name: Optional[str] = None, all: bool = False
) -> bool:
    """Drop a mongodb collection, or every collection.
    When `all`, also drops all elasticsearch indices.
    """
    all_coll_names = mongo_epigraphdb_web.list_collection_names()
    if collection_name is not None and not all:
        if collection_name in all_coll_names:
            mongo_epigraphdb_web[collection_name].drop()
        new_all_coll_names = mongo_epigraphdb_web.list_collection_names()
        res = collection_name not in new_all_coll_names
        return res
    else:
        for collection_name in all_coll_names:
            mongo_epigraphdb_web[collection_name].drop()
        es_indices: List[str] = list(es_client.indices.get_alias("*").keys())
        for index in es_indices:
            es_client.indices.delete(index=index, ignore=[400, 404])
        return True


@router.get("/utils/cache/drop/es", response_model=bool)
def get_utils_cache_drop_es() -> bool:
    """Drop all elasticsearch indices."""
    es_indices: List[str] = list(es_client.indices.get_alias("*").keys())
    for index in es_indices:
        es_client.indices.delete(index=index, ignore=[400, 404])
    return True


@router.get("/utils/cache/list", response_model=List[str])
def get_utils_cache_list() -> List[str]:
    """Returns the currently available cache collections."""
    colls = mongo_epigraphdb_web.list_collection_names()
    res = sorted(colls)
    return res
