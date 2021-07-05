from typing import Optional

from fastapi import APIRouter

from app.apis.util_routes.api import get_api_cypher
from app.models import EpigraphdbGraphsExtended
from app.models.meta_graph import EpigraphdbMetaNodeFull, EpigraphdbMetaRelFull
from app.utils import format_triple

from . import models
from .entity_resource_mapping import map_entity_resources

router = APIRouter()


@router.get(
    "/entity/resources",
    response_model=Optional[models.EntityResourcesResponse],
)
def resources_entity(
    meta_node: EpigraphdbMetaNodeFull, id: str, name: str
) -> Optional[models.EntityResources]:
    query_template = """
    MATCH
        (n:{reference_meta_node} {{_id:\"{id}\"}})-[r]-(m)
    WITH
        labels(m)[0] AS meta_node,
        type(r) AS meta_rel,
        startNode(r)._id = n._id AS reference_source_p
    RETURN DISTINCT
        meta_node, meta_rel, reference_source_p
    """
    query = query_template.format(reference_meta_node=meta_node.value, id=id)
    cypher_res = get_api_cypher(
        query=query, db=EpigraphdbGraphsExtended.epigraphdb
    )
    if cypher_res["metadata"]["empty_results"]:
        return None
    search_results = cypher_res["results"]
    triples = set(
        format_triple(
            reference_meta_node=meta_node.value,
            meta_node=_["meta_node"],
            meta_rel=_["meta_rel"],
            reference_source_p=_["reference_source_p"],
        )
        for _ in search_results
    )
    entity_resources = map_entity_resources(
        meta_node=meta_node.value,
        entity_triples=triples,
        entity_id=id,
        entity_name=name,
    )
    return entity_resources


@router.get(
    "/meta-ent/meta-node/resources",
    response_model=models.EntityResourcesResponse,
)
def meta_node_resources(
    meta_node: EpigraphdbMetaNodeFull,
) -> models.EntityResources:
    meta_ent_resources = map_entity_resources(
        meta_node=meta_node.value, meta_ent_only=True
    )
    return meta_ent_resources


@router.get(
    "/meta-ent/meta-rel/resources",
    response_model=models.EntityResourcesResponse,
)
def meta_rel_resources(
    meta_rel: EpigraphdbMetaRelFull,
) -> models.EntityResources:
    meta_ent_resources = map_entity_resources(
        meta_rel=meta_rel.value, meta_ent_only=True
    )
    return meta_ent_resources
