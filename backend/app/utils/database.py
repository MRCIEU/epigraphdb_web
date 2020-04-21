from typing import Any, Dict

from elasticsearch import Elasticsearch
from pymongo import MongoClient
from pymongo.collection import Collection

from app.settings import es_host, es_port, mongo_host, mongo_passwd, mongo_port

mongo_client = MongoClient(
    "mongodb://epigraphdb:{passwd}@{host}:{port}".format(
        passwd=mongo_passwd, host=mongo_host, port=mongo_port
    )
)

mongo_epigraphdb_web = mongo_client["epigraphdb_web"]

es_client = Elasticsearch(
    "http://{host}:{port}".format(host=es_host, port=es_port)
)


def mongo_doc_exist(collection: Collection, doc_name: str) -> bool:
    """Check if a document exists in a mongodb collection.
    The document, if exists, should be in the format
    {
       "doc_name": doc_name,
       "results": results
    }
    """
    res = collection.count_documents({"doc_name": doc_name}, limit=1) != 0
    return res


def mongo_doc_insert(collection: Collection, doc_name: str, results: Any):
    return collection.replace_one(
        filter={"doc_name": doc_name},
        replacement={"doc_name": doc_name, "results": results},
        upsert=True,
    )


def create_doc_name(params: Dict[str, Any]) -> str:
    res = "&".join([f"{key}={value}" for key, value in params.items()])
    return res


def mongo_cache_drop(master_name) -> bool:
    """Drop collections that are associated with the master name, e.g. "mr"
    """
    # list out the associated collections
    coll_names = [
        f"{master_name}_{coll}" for coll in ["response", "table", "query"]
    ]
    all_coll_names = mongo_epigraphdb_web.list_collection_names()
    # drop collections
    for coll_name in coll_names:
        if coll_name in all_coll_names:
            mongo_epigraphdb_web[coll_name].drop()
    # confirm collections have been dropped
    new_all_coll_names = mongo_epigraphdb_web.list_collection_names()
    res = (
        sum([coll_name in new_all_coll_names for coll_name in coll_names]) == 0
    )
    return res
