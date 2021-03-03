from enum import Enum
from typing import List, Optional

from fastapi import APIRouter

from app import models
from app.utils.database import es_client, mongo_cache_drop
from app.utils.logging import log_args
from app.utils.visjs_config import rels_limit

from .functions import OntologyTraitDiseaseQueryProcessor, master_name
from .index import ac_configs, ontology_trait_disease_index_name

router = APIRouter()


class OntologyTraitDiseaseAcIndex(str, Enum):
    trait = "trait"
    efo = "efo"
    disease = "disease"


@router.get("/ontology_trait_disease", response_model=bool)
def get_ontology_trait_disease(
    trait: Optional[str] = None,
    efo_term: Optional[str] = None,
    disease_label: Optional[str] = None,
    overwrite: bool = False,
) -> bool:
    """This is the master processor. For actual data use sub-apis"""
    log_args(api="/ontology_trait_disease", kwargs=locals())
    processor = OntologyTraitDiseaseQueryProcessor(
        params={
            "trait": trait,
            "efo_term": efo_term,
            "disease_label": disease_label,
            "score_threshold": 0.7,
        }
    )
    res = processor.process_master(overwrite=overwrite)
    return res


@router.get(
    "/ontology_trait_disease/{endpoint}",
    response_model=models.standard_endpoint_response,
)
def get_ontology_trait_disease_endpoints(
    endpoint: models.TopicViewEndpoints,
    trait: Optional[str] = None,
    efo_term: Optional[str] = None,
    disease_label: Optional[str] = None,
    rels_limit: int = rels_limit,
    overwrite: bool = False,
):
    log_args(api=f"/ontology_trait_disease/{endpoint.value}", kwargs=locals())
    processor = OntologyTraitDiseaseQueryProcessor(
        params={
            "trait": trait,
            "efo_term": efo_term,
            "disease_label": disease_label,
            "score_threshold": 0.7,
        }
    )
    res = None
    if endpoint.value == "table":
        res = processor.get_table_data(overwrite=overwrite)
    elif endpoint.value == "network-plot":
        res = processor.get_network_plot_data(
            rels_limit=rels_limit, overwrite=overwrite
        )
    elif endpoint.value == "query":
        res = processor.get_query_data(overwrite=overwrite)
    elif endpoint.value == "query-diagram":
        res = processor.get_query_diagram_data()
    return res


@router.get("/ontology_trait_disease/cache/drop", response_model=bool)
def get_ontology_trait_disease_cache_drop() -> bool:
    return mongo_cache_drop(master_name=master_name)


@router.get("/ontology_trait_disease/ac/index", response_model=bool)
def get_ontology_trait_disease_ac_index(overwrite: bool = False) -> bool:
    log_args(api="/ontology_trait_disease/ac/index", kwargs=locals())
    return ontology_trait_disease_index_name(overwrite=overwrite)


@router.get("/ontology_trait_disease/ac/{name}", response_model=List[str])
def get_ontology_trait_disease_ac(
    name: OntologyTraitDiseaseAcIndex, query: str, size: int = 20
) -> List[str]:
    log_args(api=f"/ontology_trait_disease/ac/{name}", kwargs=locals())
    ac_index = ac_configs[name.value]
    if not es_client.indices.exists(index=ac_index):
        get_ontology_trait_disease_ac_index()
    res = ac_configs[name]["query_fn"](
        query=query,
        index_name=ac_configs[name]["index_name"],
        es_client=es_client,
        size=size,
    )
    return res
