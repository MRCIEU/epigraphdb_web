import copy
from typing import Any, Dict, List, Set

from epigraphdb_common_utils.epigraphdb_schema import (
    meta_nodes_dict,
    resources_dict,
)
from epigraphdb_common_utils.schema_utils.models import Resource

from . import models
from .resources_extra import (
    get_api_resources_extra,
    get_rpkg_resources_extra,
    get_web_resources_extra,
)
from .web_view_urls import web_view_urls

rpkg_generic_query: models.EntityResource = {
    "key": "query_epigraphdb_{endpoint_key}",
    "name": 'query_epigraphdb(route="{route}", ...)',
    "label": "query_epigraphdb to API endpoint `{endpoint}`",
    "url": "https://mrcieu.github.io/epigraphdb-r/reference/query_epigraphdb.html",
    "queriable": False,
    "redirect_results": False,
}


def map_entity_resources(
    meta_node: str,
    triples: Set[str],
    entity_id: str,
    entity_name: str,
) -> models.EntityResources:
    resources_by_meta = meta_nodes_dict[meta_node].resources
    api_resources = []
    web_resources = []
    rpkg_resources = []
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
        )
    if resources_by_meta.rpkg is not None:
        rpkg_resources = get_rpkg_resources(
            meta_node, resources_by_meta.rpkg, triples
        )
    web_resources_extra = get_web_resources_extra(
        meta_node, entity_id, entity_name
    )
    api_resources_extra = get_api_resources_extra(
        meta_node, entity_id, entity_name
    )
    rpkg_resources_generic = get_rpkg_resources_generic(
        meta_node, api_resources
    )
    rpkg_resources_extra = get_rpkg_resources_extra(
        meta_node, entity_id, entity_name
    )
    web_resources = web_resources + web_resources_extra
    api_resources = api_resources + api_resources_extra
    rpkg_resources = (
        rpkg_resources + rpkg_resources_generic + rpkg_resources_extra
    )
    res = {"api": api_resources, "web": web_resources, "rpkg": rpkg_resources}
    return res


def get_api_resources(
    meta_node: str, resources_by_meta: Dict[str, Resource], triples: Set[str]
) -> List[models.EntityResource]:
    resources = resources_dict["api"]
    entity_api_resources = [
        {
            "key": resource_id,
            "name": resources[resource_id].label,
            "label": resources[resource_id].label,
            "url": resources[resource_id].url,
            "queriable": item.queriable,
            "redirect_results": False,
        }
        for resource_id, item in resources_by_meta.items()
        if len(triples.intersection(resources[resource_id].triples)) > 0
    ]
    if len(entity_api_resources) == 0:
        return []
    return entity_api_resources


def get_web_resources(
    meta_node: str,
    resources_by_meta: Dict[str, Resource],
    triples: Set[str],
    entity_id: str,
    entity_name: str,
) -> List[models.EntityResource]:
    resources = resources_dict["web"]
    entity_web_resources = [
        {
            "key": resource_id,
            "name": resource_id,
            "label": resources[resource_id].label,
            "url": resources[resource_id].url,
            "queriable": item.queriable,
            "redirect_results": False,
        }
        for resource_id, item in resources_by_meta.items()
        if len(triples.intersection(resources[resource_id].triples)) > 0
    ]
    if len(entity_web_resources) == 0:
        return []
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
                    entity_triples=triples,
                )
                item["redirect_results"] = True
        return entity_web_resources


def get_rpkg_resources(
    meta_node: str,
    resources_by_meta: Dict[str, Resource],
    triples: Set[str],
) -> List[models.EntityResource]:
    resources = resources_dict["rpkg"]
    entity_rpkg_resources = [
        {
            "key": resource_id,
            "name": resource_id,
            "label": resources[resource_id].label,
            "url": resources[resource_id].url,
            "queriable": item.queriable,
            "redirect_results": False,
        }
        for resource_id, item in resources_by_meta.items()
        if len(triples.intersection(resources[resource_id].triples)) > 0
    ]
    return entity_rpkg_resources


def get_rpkg_resources_generic(
    meta_node: str, api_resources: Dict[str, Any]
) -> List[models.EntityResource]:
    if api_resources is not None and len(api_resources) > 0:
        entity_rpkg_resources = []
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
        return entity_rpkg_resources
    else:
        return []
