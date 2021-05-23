from typing import Dict, List, Optional, Union

import requests
from fastapi import APIRouter
from pydash import py_

from app.apis.secondary_views.about import get_about_metrics
from app.apis.util_routes.models import (
    get_epigraphdb_meta_nodes,
    get_epigraphdb_meta_paths,
)
from app.funcs.annotate_entity import annotate_meta_entity, annotate_node_id
from app.funcs.cache import cache_func_call
from app.models.meta_graph import EpigraphdbMetaNodeFull, EpigraphdbMetaRelFull
from app.settings import api_url
from app.utils import api_request_headers
from app.utils.meta_graph import meta_node_doc_url, meta_rel_doc_url
from epigraphdb_common_utils.epigraphdb_schema import (
    meta_nodes_dict,
    meta_rels_dict,
)

from . import meta_ent_funcs, models
from .linked_resources import map_linked_external_resource

router = APIRouter()


@router.get("/meta-ent/list")
def meta_ent_list() -> Dict[str, List[models.AnnotatedMetaEntity]]:
    meta_nodes_annotated = [
        annotate_meta_entity(_, meta_entity_type="meta_node")
        for _ in get_epigraphdb_meta_nodes()
    ]
    meta_rels_annotated = [
        {
            "rel": annotate_meta_entity(_["rel"], meta_entity_type="meta_rel"),
            "source": annotate_meta_entity(
                _["source"], meta_entity_type="meta_node"
            ),
            "target": annotate_meta_entity(
                _["target"], meta_entity_type="meta_node"
            ),
        }
        for _ in get_epigraphdb_meta_paths()
    ]
    res: Dict[
        str,
        Union[
            List[models.AnnotatedMetaEntity],
            List[Dict[str, models.AnnotatedMetaEntity]],
        ],
    ] = {
        "meta_nodes": meta_nodes_annotated,
        "meta_rels": meta_rels_annotated,
    }
    return res


@router.get(
    "/meta-ent/api-endpoints-list", response_model=List[Dict[str, str]]
)
def api_endpoints_list(overwrite: bool = False) -> List[Dict[str, str]]:
    def _func():
        url = f"{api_url}/meta/api-endpoints"
        r = requests.get(url, headers=api_request_headers)
        r.raise_for_status()
        data = r.json()
        return data

    endpoints = cache_func_call(
        coll_name="entity",
        doc_name="api_endpoints",
        func=_func,
        params=None,
        overwrite=overwrite,
    )
    return endpoints


@router.get("/meta-ent/node", response_model=models.MetaNodeDataResponse)
def meta_node_data(meta_node: EpigraphdbMetaNodeFull) -> models.MetaNodeData:
    meta_node_name = meta_node.value
    metrics = get_about_metrics()
    meta_node_dict = meta_nodes_dict[meta_node_name]

    url = meta_node_doc_url(meta_node_name)
    stats = [
        {
            "stat": "count",
            "value": metrics["meta_node"][meta_node_name]["count"],
        }
    ]
    props_dict = meta_node_dict.properties
    props = [
        {
            "name": name,
            "doc": value.doc,
            "type": value.type,
            "required": value.required,
        }
        for name, value in props_dict.items()
    ]
    source_neighbours = [
        {
            "meta_node": annotate_meta_entity(
                _["from_node"], meta_entity_type="meta_node"
            ),
            "meta_rel": annotate_meta_entity(rel, meta_entity_type="meta_rel"),
            "meta_node_type": "source",
            "count": _["count"],
        }
        for rel, _ in metrics["meta_path"].items()
        if _["to_node"] == meta_node_name
    ]
    target_neighbours = [
        {
            "meta_node": annotate_meta_entity(
                _["to_node"], meta_entity_type="meta_node"
            ),
            "meta_rel": annotate_meta_entity(rel, meta_entity_type="meta_rel"),
            "meta_node_type": "target",
            "count": _["count"],
        }
        for rel, _ in metrics["meta_path"].items()
        if _["from_node"] == meta_node_name
    ]
    neighbours = source_neighbours + target_neighbours
    linked_resource = map_linked_external_resource(
        meta_node=meta_node_name, id=None
    )
    res: models.MetaNodeData = {
        "url": url,
        "id_prop": meta_node_dict.id,
        "name_prop": meta_node_dict.name,
        "props": props,
        "statistics": stats,
        "neighbours": neighbours,
        "linked_resource": linked_resource,
    }
    return res


@router.get(
    "/meta-ent/node/search", response_model=models.MetaNodeEntitySearchResponse
)
def meta_node_ent_search(
    meta_node: EpigraphdbMetaNodeFull,
    query: Optional[str] = None,
    size: int = 20,
) -> models.MetaNodeEntitySearch:
    "If query empty, simply list first few nodes"
    if query is None:
        search_results = meta_ent_funcs.list_ents(
            meta_node=meta_node, size=size
        )
    else:
        search_results = meta_ent_funcs.match_ent_by_name(
            meta_node=meta_node, name=query, size=size
        )
    items = [
        {
            "node_id": annotate_node_id(_["_id"], meta_node=meta_node),
            "node_name": _["_name"],
            "node_data": _,
        }
        for _ in search_results
    ]
    res = {
        "items": items,
    }
    return res


@router.get("/meta-ent/rel", response_model=models.MetaRelDataResponse)
def meta_rel_data(meta_rel: EpigraphdbMetaRelFull) -> models.MetaRelData:
    meta_rel_name = meta_rel.value
    metrics = get_about_metrics()
    meta_rel_dict = meta_rels_dict[meta_rel_name]

    url = meta_rel_doc_url(meta_rel_name)
    stats = [
        {"stat": "count", "value": metrics["meta_rel"][meta_rel_name]["count"]}
    ]
    props_dict = meta_rel_dict.properties
    props = [
        {
            "name": name,
            "doc": value.doc,
            "type": value.type,
            "required": value.required,
        }
        for name, value in props_dict.items()
    ]
    if len(props) == 0:
        props = None
    res = {
        "url": url,
        "source_meta_node": annotate_meta_entity(
            meta_rel_dict.source, meta_entity_type="meta_node"
        ),
        "target_meta_node": annotate_meta_entity(
            meta_rel_dict.target, meta_entity_type="meta_node"
        ),
        "props": props,
        "statistics": stats,
        "linked_resource": None,
    }
    return res


@router.get("/meta-ent/rel/search")
def meta_rel_ent_search(
    source_meta_node: EpigraphdbMetaNodeFull,
    target_meta_node: EpigraphdbMetaNodeFull,
    meta_rel: EpigraphdbMetaRelFull,
    source_query: Optional[str] = None,
    target_query: Optional[str] = None,
    size: int = 20,
):
    if source_query is None and target_query is None:
        search_results = meta_ent_funcs.list_paths(
            source_meta_node=source_meta_node.value,
            target_meta_node=target_meta_node.value,
            meta_rel=meta_rel.value,
            size=size,
        )
    else:
        search_results = meta_ent_funcs.match_path_by_name(
            source_meta_node=source_meta_node.value,
            target_meta_node=target_meta_node.value,
            meta_rel=meta_rel.value,
            source_query=source_query,
            target_query=target_query,
            size=size,
        )

    items = [
        {
            "source_node_info": {
                "id": annotate_node_id(
                    _["source"]["_id"], meta_node=source_meta_node
                ),
                "name": _["source"]["_name"],
            },
            "target_node_info": {
                "id": annotate_node_id(
                    _["target"]["_id"], meta_node=target_meta_node
                ),
                "name": _["target"]["_name"],
            },
            "source_data": _["source"],
            "target_data": _["target"],
            "rel_data": _["rel"],
        }
        for _ in search_results
    ]
    rel_cols = list(
        set(py_.flatten_deep([list(_["rel"].keys()) for _ in search_results]))
    )
    if len(rel_cols) == 0:
        rel_cols = None
    res = {
        "rel_cols": rel_cols,
        "items": items,
    }
    return res
