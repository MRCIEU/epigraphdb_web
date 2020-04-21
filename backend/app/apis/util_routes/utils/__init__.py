from fastapi import APIRouter

from app.utils.database import mongo_epigraphdb_web

router = APIRouter()


@router.get("/utils/cache/drop", response_model=bool)
def get_utils_cache_drop(collection_name: str) -> bool:
    """Drop a mongodb collection
    """
    all_coll_names = mongo_epigraphdb_web.list_collection_names()
    if collection_name in all_coll_names:
        mongo_epigraphdb_web[collection_name].drop()
    new_all_coll_names = mongo_epigraphdb_web.list_collection_names()
    res = collection_name not in new_all_coll_names
    return res
