import pandas as pd
import requests

from app.funcs.cache import cache_func_call
from app.funcs.network_graph import network_graph
from app.settings import api_key, api_url
from app.utils import api_request_headers

from .graph import GalleryGraph


def process_query(spec: GalleryGraph, overwrite: bool = False):
    coll_name = "gallery"
    doc_name = spec.name
    if spec.query_type == "cypher":
        results = cache_func_call(
            coll_name=coll_name,
            doc_name=doc_name,
            func=request_cypher,
            params=dict(query=spec.query),
            overwrite=overwrite,
        )

    if len(results) > 0:
        results_df = pd.json_normalize(results)
        graph_data = network_graph(
            df=results_df,
            node_schemas=spec.schema.nodes,
            edge_schemas=spec.schema.edges,
            limit=None,
        )
    else:
        graph_data = None

    return graph_data


def request_cypher(query: str):
    url = f"{api_url}/raw_cypher/"
    payload = {"query": query, "api_key": api_key}
    r = requests.get(url, params=payload, headers=api_request_headers)
    results = r.json()["results"]
    return results


def request_api(query: str):
    return None
