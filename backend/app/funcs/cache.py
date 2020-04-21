from typing import Any, Callable, Dict, Optional

from app.utils.database import (
    create_doc_name,
    mongo_doc_exist,
    mongo_doc_insert,
    mongo_epigraphdb_web,
)


def cache_func_call(
    coll_name: str,
    func: Callable,
    params: Optional[Dict[str, Any]],
    doc_name: Optional[str] = None,
    overwrite: bool = False,
):
    if doc_name is not None:
        doc_name_str = doc_name
    elif doc_name is None and params is not None:
        doc_name_str = create_doc_name(params=params)
    collection = mongo_epigraphdb_web[coll_name]
    res_exists = mongo_doc_exist(collection=collection, doc_name=doc_name_str)
    if overwrite or not res_exists:
        if params is None:
            res = func()
        else:
            res = func(**params)
        mongo_doc_insert(
            collection=collection, doc_name=doc_name_str, results=res
        )
    else:
        res = collection.find_one({"doc_name": doc_name_str})["results"]
    return res
