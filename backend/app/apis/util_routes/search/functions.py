from typing import Any, List

import requests

from app.funcs.elasticsearch.autocomplete import index_data
from app.settings import api_url
from app.utils import api_request_headers
from app.utils.database import es_client

from .config import search_config


def get_node_info(
    meta_node: str, total_length: int, chunk_size: int = 10000
) -> List[Any]:
    def by_chunk(url: str, offset: int, chunk_size: int) -> List[Any]:
        params = {"limit": chunk_size, "offset": offset, "full_data": False}
        r = requests.get(url, params=params, headers=api_request_headers)
        r.raise_for_status()
        return r.json()["results"]

    if total_length < chunk_size:
        chunk_size = total_length
    endpoint = f"/meta/nodes/{meta_node}/list"
    url = f"{api_url}{endpoint}"
    offset_list = [_ for _ in range(0, total_length, chunk_size)]
    nested_res = [by_chunk(url, offset, chunk_size) for offset in offset_list]
    res = [
        item
        # dict(meta_node=meta_node, **item)
        for sub_res in nested_res
        for item in sub_res
    ]
    return res


def get_index_name(meta_node: str) -> bool:
    return f"search-global-{meta_node}".lower()


def index_node_info(meta_node: str, overwrite: bool = False) -> bool:
    index_name = get_index_name(meta_node)
    input_data = get_node_info(
        meta_node=meta_node, total_length=search_config[meta_node]["length"]
    )
    index_data(
        input_data=input_data,
        index_name=index_name,
        es_client=es_client,
        indexer_fn=search_config[meta_node]["indexer"],
    )
    return True


def query_node_info(query: str, meta_node: str, size: int = 20) -> List[Any]:
    index_name = get_index_name(meta_node)
    query_body = {
        "query": {
            "match": {
                "name": {"query": query, "operator": "and", "fuzziness": 2}
            }
        },
        "size": size,
    }
    es_res = es_client.search(index=index_name, body=query_body)
    res = [item["_source"] for item in es_res["hits"]["hits"]]
    return res
