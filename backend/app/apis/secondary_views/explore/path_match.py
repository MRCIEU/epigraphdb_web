from typing import Any, Dict

import requests

from app.settings import api_url
from app.utils import api_request_headers


def path_match(
    meta_node_source: str,
    meta_node_target: str,
    id_source: str,
    id_target: str,
    max_path_length: int,
    limit: int,
):
    query_data = query_path(
        meta_node_source=meta_node_source,
        meta_node_target=meta_node_target,
        id_source=id_source,
        id_target=id_target,
        max_path_length=max_path_length,
        limit=limit,
    )
    res = query_data
    return res


def query_path(
    meta_node_source: str,
    meta_node_target: str,
    id_source: str,
    id_target: str,
    max_path_length: int,
    limit: int,
):
    url = f"{api_url}/meta/paths/search"

    params: Dict[str, Any] = {
        "meta_node_source": meta_node_source,
        "meta_node_target": meta_node_target,
        "id_source": id_source,
        "id_target": id_target,
        "max_path_length": max_path_length,
        "limit": limit,
    }

    r = requests.get(url, params=params, headers=api_request_headers)
    r.raise_for_status()

    response = r.json()
    return response
