from typing import Any, Dict, List, Optional

import requests

from app.settings import api_url


def list_ents(
    meta_node: str, size: int = 20
) -> List[Optional[Dict[str, Any]]]:
    url = f"{api_url}/meta/nodes/{meta_node}/list"
    r = requests.get(url, params={"full_data": True, "limit": size})
    r.raise_for_status()
    response_data = r.json()["results"]
    if not r.json()["metadata"]["empty_results"]:
        res = [_["n"] for _ in response_data]
        return res
    else:
        return []


def list_paths(
    source_meta_node: str, target_meta_node: str, meta_rel: str, size: int = 20
) -> List[Optional[Dict[str, Any]]]:
    url = f"{api_url}/cypher"
    query = """
    MATCH
        p=(source:{source_meta_node})
          -[rel:{meta_rel}]->
          (target:{target_meta_node})
    RETURN
         source, rel, target
    LIMIT
         {limit};
    """.format(
        source_meta_node=source_meta_node,
        target_meta_node=target_meta_node,
        meta_rel=meta_rel,
        limit=size,
    )
    r = requests.post(url, json={"query": query})
    r.raise_for_status()
    response_data = r.json()["results"]
    if not r.json()["metadata"]["empty_results"]:
        res = [_ for _ in response_data]
        return res
    else:
        return []


def match_ent_by_name(meta_node: str, name: str, size: int = 20):
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


def match_path_by_name(
    source_meta_node: str,
    target_meta_node: str,
    meta_rel: str,
    source_query: Optional[str] = None,
    target_query: Optional[str] = None,
    size: int = 20,
):
    url = f"{api_url}/cypher"
    where_clause = ""
    source_clause = None
    target_clause = None
    if source_query is not None:
        source_clause = "source._name =~ '(?i).*{name_query}.*'".format(
            name_query=source_query
        )
    if target_query is not None:
        target_clause = "target._name =~ '(?i).*{name_query}.*'".format(
            name_query=target_query
        )
    if source_clause is not None and target_clause is not None:
        where_clause = f"WHERE {source_clause} AND {target_clause}"
    elif source_clause is not None and target_clause is None:
        where_clause = f"WHERE {source_clause}"
    elif source_clause is None and target_clause is not None:
        where_clause = f"WHERE {target_clause}"
    query = """
    MATCH
        p=(source:{source_meta_node})
          -[rel:{meta_rel}]->
          (target:{target_meta_node})
    {where_clause}
    RETURN
         source, rel, target
    LIMIT
         {limit};
    """.format(
        source_meta_node=source_meta_node,
        target_meta_node=target_meta_node,
        meta_rel=meta_rel,
        where_clause=where_clause,
        limit=size,
    )
    r = requests.post(url, json={"query": query})
    r.raise_for_status()
    response_data = r.json()["results"]
    if not r.json()["metadata"]["empty_results"]:
        res = [_ for _ in response_data]
        return res
    else:
        return []
