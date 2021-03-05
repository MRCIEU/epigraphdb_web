from typing import Any, Dict, List, Optional

import requests
from fastapi import APIRouter

from app.apis.secondary_views.about.schema import (
    process_nodes_edges,
    schema_request,
)
from app.funcs.cache import cache_func_call
from app.models import EpigraphdbGraphsExtended
from app.settings import api_key, api_url
from app.utils import api_request_headers

router = APIRouter()


@router.get("/metadata/meta_node/list", response_model=List[str])
def get_metadata_meta_node_list(
    db: EpigraphdbGraphsExtended = EpigraphdbGraphsExtended.epigraphdb,
    hostname: Optional[str] = None,
    bolt_port: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    overwrite: bool = False,
) -> List[str]:
    if db.value in ["epigraphdb", "pqtl"]:
        res = cache_func_call(
            coll_name="meta_node",
            doc_name=db.value,
            func=get_meta_node,
            params={"db": db.value},
            overwrite=overwrite,
        )
    else:
        res = get_meta_node(
            db="custom",
            hostname=hostname,
            bolt_port=bolt_port,
            user=user,
            password=password,
        )
    res = sorted(res)
    return res


@router.get("/metadata/meta_rel/list", response_model=List[str])
def get_metadata_meta_rel_list(
    db: EpigraphdbGraphsExtended = EpigraphdbGraphsExtended.epigraphdb,
    hostname: Optional[str] = None,
    bolt_port: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    overwrite: bool = False,
) -> List[str]:
    if db.value in ["epigraphdb", "pqtl"]:
        res = cache_func_call(
            coll_name="meta_rel",
            doc_name=db.value,
            func=get_meta_rel,
            params={"db": db.value},
            overwrite=overwrite,
        )
    else:
        res = get_meta_rel(
            db="custom",
            hostname=hostname,
            bolt_port=bolt_port,
            user=user,
            password=password,
        )
    return res


@router.get("/metadata/meta_path/list")
def get_meta_path(overwrite: bool = False):
    nodes_data, edges_data = schema_request(overwrite=overwrite)
    nodes_df, rels_df, edges_df = process_nodes_edges(nodes_data, edges_data)
    meta_path = {
        "({from_node})-[{relationship}]-({to_node})".format(
            from_node=item["from_node"],
            relationship=item["relationship"],
            to_node=item["to_node"],
        ): {
            "from_node": item["from_node"],
            "to_node": item["to_node"],
            "relationship": item["relationship"],
        }
        for item in rels_df.to_dict(orient="records")
    }
    return meta_path


def get_meta_node(
    db: str,
    hostname: Optional[str] = None,
    bolt_port: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
) -> List[str]:
    query = "CALL db.labels()"
    url = f"{api_url}/raw_cypher/"
    params: Dict[str, Any] = {
        "query": query,
        "db": db,
        "hostname": hostname,
        "bolt_port": bolt_port,
        "user": user,
        "password": password,
        "api_key": api_key,
    }
    r = requests.get(url, params=params, headers=api_request_headers)
    r.raise_for_status()
    res = [_["label"] for _ in r.json()["results"]]
    return res


def get_meta_rel(
    db: str,
    hostname: Optional[str] = None,
    bolt_port: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
) -> List[str]:
    query = "CALL db.relationshipTypes()"
    url = f"{api_url}/raw_cypher/"
    params: Dict[str, Any] = {
        "query": query,
        "db": db,
        "hostname": hostname,
        "bolt_port": bolt_port,
        "user": user,
        "password": password,
        "api_key": api_key,
    }
    r = requests.get(url, params=params, headers=api_request_headers)
    r.raise_for_status()
    res = [_["relationshipType"] for _ in r.json()["results"]]
    return res
