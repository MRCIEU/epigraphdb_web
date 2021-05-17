from typing import Dict

import pandas as pd
import requests

from app.funcs.cache import cache_func_call
from app.settings import api_url
from app.utils import api_request_headers

from . import models


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
    meta_path_res = cache_func_call(
        coll_name="metrics",
        doc_name="meta_path",
        func=query_metric_meta_path,
        params=None,
        overwrite=overwrite,
    )

    res = {
        "meta_node": meta_node_res,
        "meta_rel": meta_rel_res,
        "meta_path": meta_path_res,
    }
    return res


def query_metric_meta_node() -> Dict[str, models.SchemaMetricsMetaNode]:
    url = f"{api_url}/status/db"
    payload = {"metric": "count_nodes_by_label", "db": "epigraphdb"}
    r = requests.get(url, params=payload, headers=api_request_headers)
    r.raise_for_status()
    # Convert from node_name: ["Gwas"] to node_name: "Gwas"
    res = {
        _["node_name"][0]: {
            "node_name": _["node_name"][0],
            "count": _["count"],
        }
        for _ in r.json()
    }
    return res


def query_metric_meta_rel() -> Dict[str, models.SchemaMetricsMetaRel]:
    url = f"{api_url}/status/db"
    payload = {"metric": "count_rels_by_type", "db": "epigraphdb"}
    r = requests.get(url, params=payload, headers=api_request_headers)
    r.raise_for_status()
    res = {_["relationshipType"]: _ for _ in r.json()}
    return res


def query_metric_meta_path() -> Dict[str, models.SchemaMetricsMetaPath]:
    url = f"{api_url}/meta/schema"
    params = {"graphviz": False, "plot": False}
    r = requests.get(url, params=params, headers=api_request_headers)
    r.raise_for_status()
    data = r.json()
    res = (
        pd.json_normalize(data["connections"])
        .assign(index=lambda df: df["rel"])
        .set_index("index")
    ).to_dict(orient="index")
    return res
