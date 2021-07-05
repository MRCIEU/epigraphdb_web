import copy
from typing import Dict, List, Optional, Set

from epigraphdb_common_utils.epigraphdb_schema import (
    meta_nodes_dict,
    meta_rels_dict,
    resources_dict,
)
from epigraphdb_common_utils.schema_utils.models import Resource

from . import models
from .resources_extra import (
    get_api_resources_extra,
    get_rpkg_resources_extra,
    get_web_resources_extra,
)

rpkg_generic_query: models.EntityResource = {
    "key": "query_epigraphdb_{endpoint_key}",
    "name": 'query_epigraphdb(route="{route}", ...)',
    "label": "query_epigraphdb to API endpoint `{endpoint}`",
    "url": "https://mrcieu.github.io/epigraphdb-r/reference/query_epigraphdb.html",
    "queriable": False,
}


def map_entity_resources(
    meta_node: Optional[str] = None,
    meta_rel: Optional[str] = None,
    entity_triples: Optional[Set[str]] = None,
    entity_id: Optional[str] = None,
    entity_name: Optional[str] = None,
    meta_ent_only: bool = False,
) -> models.EntityResources:
    """Use in the following ways:

    - resources for an entity node,
      provide `meta_node`, `entity_triples`, `entity_id`, `entity_name`,
      and `meta_ent_only` = False
    - resources for a meta node,
      provide `meta_node`, and `meta_ent_only` = True
    - resources for a meta rel,
      provide `meta_rel`, and `meta_ent_only` = True
    """
    # exception handling
    if meta_ent_only:
        if meta_node is None and meta_rel is None:
            raise Exception("`meta_node` and `meta_rel` can't be both None")
    else:
        if meta_node is None:
            raise Exception("`meta_node` can't be None")
        if entity_id is None or entity_name is None or entity_triples is None:
            raise Exception("Missing entity info")
    if meta_node is not None:
        resources_by_meta = meta_nodes_dict[meta_node].resources
    else:
        resources_by_meta = meta_rels_dict[meta_rel].resources
    api_resources = []
    web_resources = []
    rpkg_resources = []
    rpkg_resources_generic = []
    api_resources_extra = []
    web_resources_extra = []
    rpkg_resources_extra = []
    if resources_by_meta.api is not None:
        api_resources = get_api_resources(
            resources_by_meta.api, entity_triples, meta_ent_only
        )
        rpkg_resources_generic = get_rpkg_resources_generic(api_resources)
    if resources_by_meta.web is not None:
        web_resources = get_web_resources(
            resources_by_meta.web,
            entity_triples,
            meta_ent_only,
        )
    if resources_by_meta.rpkg is not None:
        rpkg_resources = get_rpkg_resources(
            resources_by_meta.rpkg,
            entity_triples,
            meta_ent_only,
        )
    if meta_node is not None:
        web_resources_extra = get_web_resources_extra(
            meta_node, entity_id, entity_name, meta_ent_only
        )
        api_resources_extra = get_api_resources_extra(
            meta_node, entity_id, entity_name, meta_ent_only
        )
        rpkg_resources_extra = get_rpkg_resources_extra(
            meta_node, entity_id, entity_name, meta_ent_only
        )
    web_resources = web_resources + web_resources_extra
    api_resources = api_resources + api_resources_extra
    rpkg_resources = (
        rpkg_resources + rpkg_resources_generic + rpkg_resources_extra
    )
    res = {"api": api_resources, "web": web_resources, "rpkg": rpkg_resources}
    return res


def get_api_resources(
    resources_by_meta: Dict[str, Resource],
    entity_triples: Optional[Set[str]],
    meta_ent_only: bool = False,
) -> List[models.EntityResource]:
    resources = resources_dict["api"]
    entity_api_resources: List[models.EntityResource] = [
        {
            "key": resource_id,
            "name": resources[resource_id].label,
            "label": resources[resource_id].label,
            "url": resources[resource_id].url,
            "queriable": resource_item.queriable,
        }
        for resource_id, resource_item in resources_by_meta.items()
        if is_entity_associated_with_resource(
            entity_triples=entity_triples,
            resource_triples=resources[resource_id].triples,
            meta_ent_only=meta_ent_only,
        )
    ]
    return entity_api_resources


def get_web_resources(
    resources_by_meta: Dict[str, Resource],
    entity_triples: Optional[Set[str]],
    meta_ent_only: bool = False,
) -> List[models.EntityResource]:
    resources = resources_dict["web"]
    entity_web_resources: List[models.EntityResource] = [
        {
            "key": resource_id,
            "name": resource_id,
            "label": resources[resource_id].label,
            "url": resources[resource_id].url,
            "queriable": resource_item.queriable,
        }
        for resource_id, resource_item in resources_by_meta.items()
        if is_entity_associated_with_resource(
            entity_triples=entity_triples,
            resource_triples=resources[resource_id].triples,
            meta_ent_only=meta_ent_only,
        )
    ]
    return entity_web_resources


def get_rpkg_resources(
    resources_by_meta: Dict[str, Resource],
    entity_triples: Optional[Set[str]],
    meta_ent_only: bool = False,
) -> List[models.EntityResource]:
    resources = resources_dict["rpkg"]
    entity_rpkg_resources = [
        {
            "key": resource_id,
            "name": resource_id,
            "label": resources[resource_id].label,
            "url": resources[resource_id].url,
            "queriable": resource_item.queriable,
        }
        for resource_id, resource_item in resources_by_meta.items()
        if is_entity_associated_with_resource(
            entity_triples=entity_triples,
            resource_triples=resources[resource_id].triples,
            meta_ent_only=meta_ent_only,
        )
    ]
    return entity_rpkg_resources


def get_rpkg_resources_generic(
    api_resources: List[models.EntityResource],
) -> List[models.EntityResource]:
    def _process(api_resource):
        route = api_resource["label"].split(" ")[1]
        rpkg_equivalent = copy.deepcopy(rpkg_generic_query)
        rpkg_equivalent["name"] = rpkg_equivalent["name"].format(route=route)
        rpkg_equivalent["key"] = rpkg_equivalent["key"].format(
            endpoint_key=api_resource["key"]
        )
        rpkg_equivalent["label"] = rpkg_equivalent["label"].format(
            endpoint=api_resource["label"]
        )
        rpkg_equivalent["queriable"] = api_resource["queriable"]
        return rpkg_equivalent

    entity_rpkg_resources = [
        _process(api_resource) for api_resource in api_resources
    ]
    return entity_rpkg_resources


def is_entity_associated_with_resource(
    entity_triples: Optional[Set[str]],
    resource_triples: Set[str],
    meta_ent_only: bool = False,
) -> bool:
    # resources contain meta entity (schema) level triples,
    # but not every entity has that triple.
    #
    # returns True when entity has the schema level triples
    # and therefore the resource is associated with the entity
    #
    # When `meta_ent_only`: skip this
    if meta_ent_only:
        return True
    intersection = entity_triples.intersection(resource_triples)
    res = len(intersection) > 0
    return res
