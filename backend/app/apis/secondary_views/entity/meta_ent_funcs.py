from typing import Any, Dict, List, Optional

import requests

from app.settings import api_url


def list_ents(meta_node: str, size=20) -> List[Optional[Dict[str, Any]]]:
    url = f"{api_url}/meta/nodes/{meta_node}/list"
    r = requests.get(url, params={"full_data": True, "limit": size})
    r.raise_for_status()
    response_data = r.json()["results"]
    if not r.json()["metadata"]["empty_results"]:
        res = [_["n"] for _ in response_data]
        return res
    else:
        return []


def match_ent_by_name(meta_node: str, name: str, size=20):
    url = f"{api_url}/meta/nodes/{meta_node}/search"
    r = requests.get(
        url, params={"full_data": True, "name": name, "limit": size}
    )
    r.raise_for_status()
    response_data = r.json()["results"]
    if not r.json()["metadata"]["empty_results"]:
        res = [_["node"] for _ in response_data]
        return res
    else:
        return []
