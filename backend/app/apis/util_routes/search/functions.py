from typing import Any, List, Optional

import requests

from app.funcs.elasticsearch.autocomplete import index_data
from app.settings import api_url
from app.utils import api_request_headers
from app.utils.database import es_client

from .config import search_config
from .models import EpigraphdbMetaNodeForSearch


def get_node_info(
    meta_node: str, total_length: int, chunk_size: int = 10_000
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
        {"id": item["id"], "name": item["name"], "meta_node": meta_node}
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
    if overwrite:
        es_client.indices.delete(index=index_name, ignore=[400, 404])
    index_data(
        input_data=input_data,
        index_name=index_name,
        es_client=es_client,
        indexer_fn=search_config[meta_node]["indexer"],
    )
    return True


def query_node_info(
    query: str, meta_node: Optional[str], size: int = 20
) -> List[Any]:
    if meta_node is not None:
        index = get_index_name(meta_node)
    else:
        index = [get_index_name(_.value) for _ in EpigraphdbMetaNodeForSearch]
    query_body = {
        "query": {
            "match": {
                "name": {"query": query, "operator": "and", "fuzziness": 2}
            }
        },
        # When search across all entities, always boost items from Gwas
        "indices_boost": [{get_index_name("Gwas"): 3.5}],
        "size": size,
    }
    es_res = es_client.search(index=index, body=query_body)
    res = [item["_source"] for item in es_res["hits"]["hits"]]
    return res
