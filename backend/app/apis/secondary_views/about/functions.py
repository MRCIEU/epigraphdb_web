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

    res = cache_func_call(
        coll_name="metadata",
        doc_name="metadata",
        func=query_func,
        params=None,
        overwrite=overwrite,
    )
    return res


def get_metrics(overwrite: bool = False):

    meta_node_res = cache_func_call(
        coll_name="metrics",
        doc_name="meta_node",
        func=query_metric_meta_node,
        params=None,
        overwrite=overwrite,
    )
    meta_rel_res = cache_func_call(
        coll_name="metrics",
        doc_name="meta_rel",
        func=query_metric_meta_rel,
        params=None,
        overwrite=overwrite,
    )

    res = {"meta_node": meta_node_res, "meta_rel": meta_rel_res}
    return res


def query_metric_meta_node():
    url = f"{api_url}/status/db"
    payload = {"metric": "count_nodes_by_label", "db": "epigraphdb"}
    r = requests.get(url, params=payload)
    r.raise_for_status()
    # Convert from node_name: ["Gwas"] to node_name: "Gwas"
    res = [
        {"node_name": _["node_name"][0], "count": _["count"]} for _ in r.json()
    ]
    return res


def query_metric_meta_rel():
    url = f"{api_url}/status/db"
    payload = {"metric": "count_rels_by_type", "db": "epigraphdb"}
    r = requests.get(url, params=payload)
    r.raise_for_status()
    res = r.json()
    return res
