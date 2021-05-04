import operator
from functools import reduce
from typing import List, Optional

import requests
from fastapi import APIRouter, Query

from app.apis.util_routes.api import get_api_cypher
from app.funcs.annotate_entity import (
    annotate_meta_entity,
    annotate_node_id,
    annotate_property,
)
from app.models import EpigraphdbGraphsExtended
from app.models.meta_graph import EpigraphdbMetaNodeFull
from app.settings import api_url
from app.utils import api_request_headers, format_triple, get_node_role

from . import models
from .entity_resource_mapping import map_entity_resources
from .linked_resources import map_linked_external_resource

router = APIRouter()

NODE_META_PROPS = ["_id", "_name", "_source"]


@router.get(
    "/entity/search/node", response_model=models.EntitySearchNodeResponse
)
def entity_search_node(
    meta_node: EpigraphdbMetaNodeFull, id: str
) -> Optional[models.EntitySearchNode]:
    url = f"{api_url}/meta/nodes/{meta_node.value}/search"
    params = {"id": id, "full_data": True}
    r = requests.get(url, params=params, headers=api_request_headers)
    r.raise_for_status()
    data = r.json()["results"]
    if len(data) == 0:
        return None
    else:
        node = data[0]["node"]
        linked_resource = map_linked_external_resource(
            meta_node=meta_node.value, id=id
        )
        res: models.EntitySearchNode = {
            "meta_node": annotate_meta_entity(
                meta_node.value, meta_entity_type="meta_node"
            ),
            "entity_id": node["_id"],
            "entity_name": node["_name"],
            "entity_source": node["_source"],
            "full_data": [
                {
                    "key": key,
                    "annotation": annotate_property(
                        prop_name=key,
                        meta_entity=meta_node.value,
                        meta_entity_type="node",
                    ),
                    "value": value,
                }
                for key, value in node.items()
                if key not in NODE_META_PROPS
            ],
            "linked_resource": linked_resource,
        }
        print(res)
    return res


@router.get(
    "/entity/meta-neighbours",
    response_model=Optional[models.EntityMetaNeighboursResponse],
)
def entity_meta_neighbours(
    meta_node: EpigraphdbMetaNodeFull, id: str, name: str
) -> Optional[models.EntityMetaNeighbours]:
    # NOTE: for is_target checking against n._id is way
    # faster than m._id
    query_template = """
    MATCH
        (n:{meta_node} {{_id:\"{id}\"}})-[r]-(m)
    RETURN
        labels(m)[0] AS meta_node,
        type(r) AS meta_rel,
        startNode(r)._id = n._id AS is_n_source,
        count(*) AS count
    """
    query = query_template.format(meta_node=meta_node.value, id=id)
    cypher_res = get_api_cypher(
        query=query, db=EpigraphdbGraphsExtended.epigraphdb
    )
    if cypher_res["metadata"]["empty_results"]:
        return None
    else:
        full_data_raw = cypher_res["results"]
        meta_node_list = sorted(
            list(set([_["meta_node"] for _ in full_data_raw]))
        )
        meta_rel_list = sorted(
            list(set([_["meta_rel"] for _ in full_data_raw]))
        )
        full_data = [
            {
                "meta_node": annotate_meta_entity(
                    _["meta_node"], meta_entity_type="meta_node"
                ),
                "meta_rel": annotate_meta_entity(
                    _["meta_rel"], meta_entity_type="meta_rel"
                ),
                "meta_node_type": get_node_role(_["is_n_source"]),
                "count": _["count"],
            }
            for _ in full_data_raw
        ]
        triples = set(
            format_triple(
                meta_node.value,
                _["meta_node"]["name"],
                _["meta_rel"]["name"],
                _["meta_node_type"],
            )
            for _ in full_data
        )
        # For now only do binary case and prefers source when reference is both
        # source and target
        reference_is_source = reduce(
            operator.__or__, [_["is_n_source"] for _ in full_data_raw]
        )
        entity_node_type = "source" if reference_is_source else "target"
        entity_resources = map_entity_resources(
            meta_node.value,
            triples,
            entity_id=id,
            entity_name=name,
            entity_node_type=entity_node_type,
        )
        res = {
            "meta_node_list": meta_node_list,
            "meta_rel_list": meta_rel_list,
            "entity_resources": entity_resources,
            "full_data": full_data,
        }
        return res


@router.get(
    "/entity/neighbours",
    response_model=Optional[List[models.EntityNeighbourResponse]],
)
def entity_neighbours(
    meta_node: EpigraphdbMetaNodeFull,
    id: str,
    filter_meta_rel: Optional[str] = None,
    filter_meta_node: Optional[EpigraphdbMetaNodeFull] = None,
    filter_node_type: Optional[models.EntityNodeType] = None,
    limit: int = Query(50, gt=0, lt=500),
) -> Optional[List[models.EntityNeighbour]]:
    query_template = """
    MATCH
        (n:{meta_node} {{_id:\"{id}\"}})
        -{filter_meta_rel_expr}-
        {filter_meta_node_expr}
    {filter_clause}
    RETURN
        labels(m)[0] AS meta_node,
        type(r) AS meta_rel,
        startNode(r)._id = n._id AS is_n_source,
        m._id AS node_id,
        m._name AS node_name
    LIMIT {limit}
    """
    if filter_meta_node is None:
        filter_meta_node_expr = "(m)"
    else:
        filter_meta_node_expr = f"(m: {filter_meta_node})"
    if filter_meta_rel is None:
        filter_meta_rel_expr = "[r]"
    else:
        filter_meta_rel_expr = f"[r:{filter_meta_rel}]"
    if filter_node_type is None:
        filter_clause = ""
    elif filter_node_type == models.EntityNodeType.source:
        filter_clause = "WHERE startNode(r)._id <> n._id"
    else:
        filter_clause = "WHERE startNode(r)._id = n._id"
    query = query_template.format(
        meta_node=meta_node.value,
        id=id,
        filter_meta_node_expr=filter_meta_node_expr,
        filter_meta_rel_expr=filter_meta_rel_expr,
        filter_clause=filter_clause,
        limit=limit,
    )
    cypher_res = get_api_cypher(
        query=query, db=EpigraphdbGraphsExtended.epigraphdb
    )
    if cypher_res["metadata"]["empty_results"]:
        return None
    else:
        data_raw = cypher_res["results"]
        res = [
            {
                "meta_node": annotate_meta_entity(
                    _["meta_node"], meta_entity_type="meta_node"
                ),
                "meta_rel": annotate_meta_entity(
                    _["meta_rel"], meta_entity_type="meta_rel"
                ),
                "node_id": annotate_node_id(
                    _["node_id"], meta_node=_["meta_node"]
                ),
                "node_name": _["node_name"],
                "node_type": get_node_role(_["is_n_source"]),
            }
            for _ in data_raw
        ]
        return res