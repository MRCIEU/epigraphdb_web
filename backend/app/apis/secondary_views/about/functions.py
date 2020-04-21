import requests

from app.funcs.cache import cache_func_call
from app.settings import api_url


def get_metadata(overwrite: bool = False):
    def query_func():
        url = f"{api_url}/status/db"
        payload = {"metric": "graph_metadata", "db": "epigraphdb"}
        r = requests.get(url, params=payload)
        r.raise_for_status()
        res = r.json()
        return res

    doc_name = "metadata"
    coll_name = "metadata"
    res = cache_func_call(
        coll_name=coll_name,
        doc_name=doc_name,
        func=query_func,
        params=None,
        overwrite=overwrite,
    )
    return res
