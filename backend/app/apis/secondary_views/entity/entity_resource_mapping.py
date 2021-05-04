import copy
from typing import Dict, List, Optional, Set

from epigraphdb_common_utils.epigraphdb_schema import (
    meta_nodes_dict,
    resources_dict,
)
from epigraphdb_common_utils.schema_utils.models import Resource

from . import models
from .web_view_urls import web_view_urls

rpkg_generic_query: models.EntityResource = {
    "key": "query_epigraphdb_{endpoint_key}",
    "name": 'query_epigraphdb(route="{route}", ...)',
    "label": "query_epigraphdb to API endpoint `{endpoint}`",
    "url": "https://mrcieu.github.io/epigraphdb-r/reference/query_epigraphdb.html",
    "queriable": False,
}


def map_entity_resources(
    meta_node: str,
    triples: Set[str],
    entity_id: str,
    entity_name: str,
    entity_node_type: str,
) -> models.EntityResources:
    resources_by_meta = meta_nodes_dict[meta_node].resources
    api_resources = None
    web_resources = None
    rpkg_resources = None
    if resources_by_meta.api is not None:
        api_resources = get_api_resources(
            meta_node, resources_by_meta.api, triples
        )
    if resources_by_meta.web is not None:
        web_resources = get_web_resources(
            meta_node,
            resources_by_meta.web,
            triples,
            entity_id,
            entity_name,
            entity_node_type,
        )
    if resources_by_meta.rpkg is not None:
        rpkg_resources = get_rpkg_resources(
            meta_node, resources_by_meta.rpkg, api_resources, triples
        )
    res = {"api": api_resources, "web": web_resources, "rpkg": rpkg_resources}
    return res


def get_api_resources(
    meta_node: str, resources_by_meta: Dict[str, Resource], triples: Set[str]
) -> Optional[List[models.EntityResource]]:
    resources = resources_dict["api"]
    entity_api_resources = [
        {
            "key": resource_id,
            "name": resource_id,
            "label": resources[resource_id].label,
            "url": resources[resource_id].url,
            "queriable": item.queriable,
        }
        for resource_id, item in resources_by_meta.items()
        if len(triples.intersection(resources[resource_id].triples)) > 0
    ]
    if len(entity_api_resources) == 0:
        return None
    return entity_api_resources


def get_web_resources(
    meta_node: str,
    resources_by_meta: Dict[str, Resource],
    triples: Set[str],
    entity_id: str,
    entity_name: str,
    entity_node_type: str,
) -> Optional[List[models.EntityResource]]:
    resources = resources_dict["web"]
    entity_web_resources = [
        {
            "key": resource_id,
            "name": resource_id,
            "label": resources[resource_id].label,
            "url": resources[resource_id].url,
            "queriable": item.queriable,
        }
        for resource_id, item in resources_by_meta.items()
        if len(triples.intersection(resources[resource_id].triples)) > 0
    ]
    if len(entity_web_resources) == 0:
        return None
    else:
        for item in entity_web_resources:
            if (
                item["key"] in web_view_urls.keys()
                and meta_node in web_view_urls[item["key"]].keys()
            ):
                url_generator = web_view_urls[item["key"]][meta_node]
                item["url"] = url_generator.generate_url(
                    root_url=item["url"],
                    entity_id=entity_id,
                    entity_name=entity_name,
                    entity_node_type=entity_node_type,
                )
        return entity_web_resources


def get_rpkg_resources(
    meta_node: str,
    resources_by_meta: Dict[str, Resource],
    api_resources: Optional[Dict[str, Resource]],
    triples: Set[str],
) -> Optional[List[models.EntityResource]]:
    resources = resources_dict["rpkg"]
    entity_rpkg_resources = [
        {
            "key": resource_id,
            "name": resource_id,
            "label": resources[resource_id].label,
            "url": resources[resource_id].url,
            "queriable": item.queriable,
        }
        for resource_id, item in resources_by_meta.items()
        if len(triples.intersection(resources[resource_id].triples)) > 0
    ]
    if api_resources is not None and len(api_resources) > 0:
        for api_resource in api_resources:
            route = api_resource["label"].split(" ")[1]
            rpkg_equivalent = copy.deepcopy(rpkg_generic_query)
            rpkg_equivalent["name"] = rpkg_equivalent["name"].format(
                route=route
            )
            rpkg_equivalent["key"] = rpkg_equivalent["key"].format(
                endpoint_key=api_resource["key"]
            )
            rpkg_equivalent["label"] = rpkg_equivalent["label"].format(
                endpoint=api_resource["label"]
            )
            rpkg_equivalent["queriable"] = api_resource["queriable"]
            entity_rpkg_resources.append(rpkg_equivalent)
    if len(entity_rpkg_resources) == 0:
        return None
    return entity_rpkg_resources
