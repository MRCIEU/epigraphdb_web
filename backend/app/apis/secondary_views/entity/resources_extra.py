from typing import Any, Dict, List, Optional
from urllib.parse import quote, urlencode

from app.apis.topic_views.covid_xqtl import get_list_ctda
from app.apis.topic_views.covid_xqtl import models as covid_xqtl_models
from app.apis.topic_views.pqtl import (
    PQTLSearchType,
    get_pqtl_list,
    get_pqtl_list_outcome,
)
from epigraphdb_common_utils.epigraphdb_schema import resources_extra_dict
from epigraphdb_common_utils.schema_utils.processing import (
    api_url_formatter,
    rpkg_url_formatter,
)

from . import models
from .trait_id_translators import (
    opengwas_id_to_covid_xqtl_mrbase_id,
    opengwas_id_to_pqtl_mrbase_id,
)


def pqtl_trait_mapper(entity_id: str, entity_name: str) -> Optional[str]:
    mrbase_id = opengwas_id_to_pqtl_mrbase_id(entity_id)
    if mrbase_id is None:
        return None
    else:
        pqtl_outcomes = {
            _["mrbase_id"]: _["label"] for _ in get_pqtl_list_outcome()
        }
        if mrbase_id not in pqtl_outcomes.keys():
            return None
        else:
            return pqtl_outcomes[mrbase_id]


def pqtl_gene_mapper(entity_id: str, entity_name: str) -> Optional[str]:
    pqtl_outcomes = get_pqtl_list(PQTLSearchType.exposures)
    if entity_name not in pqtl_outcomes:
        return None
    else:
        return entity_name


def covid_xqtl_trait_mapper(entity_id: str, entity_name: str) -> Optional[str]:
    mrbase_id = opengwas_id_to_covid_xqtl_mrbase_id(entity_id)
    if mrbase_id is None:
        return None
    else:
        ents_list = get_list_ctda(covid_xqtl_models.CovidXqtlList.gwas)
        ent_ids = [_["id"] for _ in ents_list]
        if mrbase_id not in ent_ids:
            return None
        else:
            return mrbase_id


def covid_xqtl_gene_mapper(entity_id: str, entity_name: str) -> Optional[str]:
    ents_list = get_list_ctda(covid_xqtl_models.CovidXqtlList.gene)
    ent_ids = [_["id"] for _ in ents_list]
    if entity_id not in ent_ids:
        return None
    else:
        return entity_id


def covid_xqtl_tissue_mapper(
    entity_id: str, entity_name: str
) -> Optional[str]:
    ents_list = get_list_ctda(covid_xqtl_models.CovidXqtlList.tissue)
    ent_ids = [_["name"] for _ in ents_list]
    transformed_id = entity_id.replace(" - ", "_").replace(" ", "_")
    if transformed_id not in ent_ids:
        return None
    else:
        return transformed_id


def covid_xqtl_snp_mapper(entity_id: str, entity_name: str) -> Optional[str]:
    ents_list = get_list_ctda(covid_xqtl_models.CovidXqtlList.snp)
    ent_ids = [_["name"] for _ in ents_list]
    if entity_id not in ent_ids:
        return None
    else:
        return entity_id


def pqtl_url_generator(
    entity: str, meta_node: str, queriable: bool = True
) -> str:
    pqtl_url = "https://epigraphdb.org/pqtl/"
    if queriable:
        url_template = "{pqtl_url}{entity}"
        return url_template.format(pqtl_url=pqtl_url, entity=quote(entity))
    else:
        return pqtl_url


def covid_xqtl_url_generator(
    entity: str, meta_node: str, queriable: bool = True
) -> str:
    covid_xqtl_url = "https://epigraphdb.org/covid-19/ctda"
    if queriable:
        url_template = "{covid_xqtl_url}/?{query_expr}"
        meta_node_mapping = {
            "Gwas": "gwas",
            "Gene": "gene",
            "Tissue": "tissue",
        }
        node = meta_node_mapping[meta_node]
        query_expr = urlencode({node: entity})
        return url_template.format(
            covid_xqtl_url=covid_xqtl_url, query_expr=query_expr
        )
    return covid_xqtl_url


entity_mappers = {
    "pqtl_trait_mapper": pqtl_trait_mapper,
    "pqtl_gene_mapper": pqtl_gene_mapper,
    "covid_xqtl_trait_mapper": covid_xqtl_trait_mapper,
    "covid_xqtl_gene_mapper": covid_xqtl_gene_mapper,
    "covid_xqtl_tissue_mapper": covid_xqtl_tissue_mapper,
    "covid_xqtl_snp_mapper": covid_xqtl_snp_mapper,
}

url_generators = {
    "pqtl_url_generator": pqtl_url_generator,
    "covid_xqtl_url_generator": covid_xqtl_url_generator,
}


def get_web_resources_extra(
    meta_node: str, entity_id: str, entity_name: str
) -> List[models.EntityResource]:
    if meta_node not in resources_extra_dict["nodes"].keys():
        return []
    else:
        assoc_ent_list = resources_extra_dict["nodes"][meta_node]
        res = [
            map_web_resource(meta_node, entity_id, entity_name, assoc_ent_info)
            for assoc_ent_info in assoc_ent_list
        ]
        res = [_ for _ in res if _ is not None]
        return res


def get_api_resources_extra(
    meta_node: str, entity_id: str, entity_name: str
) -> List[models.EntityResource]:
    if meta_node not in resources_extra_dict["nodes"].keys():
        return []
    else:
        assoc_ent_list = resources_extra_dict["nodes"][meta_node]
        res = [
            map_api_resource(meta_node, entity_id, entity_name, assoc_ent_info)
            for assoc_ent_info in assoc_ent_list
        ]
        res = [_ for _ in res if _ is not None]
        return res


def get_rpkg_resources_extra(
    meta_node: str, entity_id: str, entity_name: str
) -> List[models.EntityResource]:
    if meta_node not in resources_extra_dict["nodes"].keys():
        return []
    else:
        assoc_ent_list = resources_extra_dict["nodes"][meta_node]
        res = [
            map_rpkg_resource(
                meta_node, entity_id, entity_name, assoc_ent_info
            )
            for assoc_ent_info in assoc_ent_list
        ]
        res = [_ for _ in res if _ is not None]
        return res


def map_web_resource(
    meta_node: str,
    entity_id: str,
    entity_name: str,
    assoc_ent_info: Dict[str, Any],
) -> Optional[models.EntityResource]:
    assoc_ent_name = assoc_ent_info["assoc_ent"]
    resource_name = resources_extra_dict["assoc_ents"][assoc_ent_name]["web"]
    if resource_name is None:
        return None
    resource = resources_extra_dict["assoc_resources"]["web"][resource_name]
    entity_mapper_fn = entity_mappers[assoc_ent_info["mapper"]]
    assoc_entity = entity_mapper_fn(entity_id, entity_name)
    queriable = assoc_ent_info["queriable"]
    if assoc_entity is None:
        return None
    else:
        url_generator_fn = url_generators[resource["url_fn"]]
        url = url_generator_fn(
            entity=assoc_entity, meta_node=meta_node, queriable=queriable
        )
        res: models.EntityResource = {
            "key": resource_name,
            "name": resource["name"],
            "label": resource["label"],
            "url": url,
            "queriable": queriable,
            # if queriable, then for resources_extra it is
            # sufficient for it to contain results
            "redirect_results": queriable,
        }
        return res


def map_api_resource(
    meta_node: str,
    entity_id: str,
    entity_name: str,
    assoc_ent_info: Dict[str, Any],
) -> Optional[models.EntityResource]:
    assoc_ent_name = assoc_ent_info["assoc_ent"]
    resource_name = resources_extra_dict["assoc_ents"][assoc_ent_name]["api"]
    if resource_name is None:
        return None
    resource = resources_extra_dict["assoc_resources"]["api"][resource_name]
    entity_mapper_fn = entity_mappers[assoc_ent_info["mapper"]]
    assoc_entity = entity_mapper_fn(entity_id, entity_name)
    queriable = assoc_ent_info["queriable"]
    if assoc_entity is None:
        return None
    else:
        url = api_url_formatter(uri=resource["uri"])
        res: models.EntityResource = {
            "key": resource_name,
            "name": resource["name"],
            "label": resource["label"],
            "url": url,
            "queriable": queriable,
            "redirect_results": False,
        }
        return res


def map_rpkg_resource(
    meta_node: str,
    entity_id: str,
    entity_name: str,
    assoc_ent_info: Dict[str, Any],
) -> Optional[models.EntityResource]:
    assoc_ent_name = assoc_ent_info["assoc_ent"]
    resource_name = resources_extra_dict["assoc_ents"][assoc_ent_name]["rpkg"]
    if resource_name is None:
        return None
    resource = resources_extra_dict["assoc_resources"]["rpkg"][resource_name]
    entity_mapper_fn = entity_mappers[assoc_ent_info["mapper"]]
    assoc_entity = entity_mapper_fn(entity_id, entity_name)
    queriable = assoc_ent_info["queriable"]
    if assoc_entity is None:
        return None
    else:
        url = rpkg_url_formatter(uri=resource["uri"])
        res: models.EntityResource = {
            "key": resource_name,
            "name": resource["name"],
            "label": resource["label"],
            "url": url,
            "queriable": queriable,
            "redirect_results": False,
        }
        return res
