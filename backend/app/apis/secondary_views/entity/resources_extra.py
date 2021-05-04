from typing import Any, Dict, List, Optional
from urllib.parse import quote

from app.apis.topic_views.pqtl import (
    PQTLSearchType,
    get_pqtl_list,
    get_pqtl_list_outcome,
)
from epigraphdb_common_utils.epigraphdb_schema import resources_extra_dict

from . import models
from .trait_id_translators import opengwas_id_to_pqtl_mrbase_id


def pqtl_trait_mapper(entity_id: str, entity_name: str) -> Optional[str]:
    pqtl_mrbase_id = opengwas_id_to_pqtl_mrbase_id(entity_id)
    if pqtl_mrbase_id is None:
        return None
    else:
        pqtl_outcomes = {
            _["mrbase_id"]: _["label"] for _ in get_pqtl_list_outcome()
        }
        if pqtl_mrbase_id not in pqtl_outcomes.keys():
            return None
        else:
            return pqtl_outcomes[pqtl_mrbase_id]


def pqtl_gene_mapper(entity_id: str, entity_name: str) -> Optional[str]:
    pqtl_outcomes = get_pqtl_list(PQTLSearchType.exposures)
    if entity_name not in pqtl_outcomes:
        return None
    else:
        return entity_name


def pqtl_url_generator(entity: str) -> str:
    url_template = "https://epigraphdb.org/pqtl/{entity}"
    return url_template.format(entity=quote(entity))


entity_mappers = {
    "pqtl_trait_mapper": pqtl_trait_mapper,
    "pqtl_gene_mapper": pqtl_gene_mapper,
}

url_generators = {"pqtl_url_generator": pqtl_url_generator}


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


def map_web_resource(
    meta_node: str,
    entity_id: str,
    entity_name: str,
    assoc_ent_info: Dict[str, Any],
) -> Optional[models.EntityResource]:
    assoc_ent_name = assoc_ent_info["assoc_ent"]
    resource_name = resources_extra_dict["assoc_ents"][assoc_ent_name]["web"]
    resource = resources_extra_dict["assoc_resources"]["web"][resource_name]
    entity_mapper_fn = entity_mappers[assoc_ent_info["mapper"]]
    url_generator_fn = url_generators[resource["url_fn"]]
    assoc_entity = entity_mapper_fn(entity_id, entity_name)
    if assoc_entity is None:
        return None
    else:
        url = url_generator_fn(entity=assoc_entity)
        res: models.EntityResource = {
            "key": resource["name"],
            "name": resource["name"],
            "label": resource["label"],
            "url": url,
            "queriable": True,
        }
        return res
