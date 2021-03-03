from typing import List

from fastapi import APIRouter, Query

from app import models
from app.funcs.elasticsearch.autocomplete import index_ac_name_from_cypher
from app.funcs.elasticsearch.query import query_ac_name
from app.utils.database import es_client, mongo_cache_drop
from app.utils.logging import log_args
from app.utils.visjs_config import rels_limit

from .functions import ObsCorQueryProcessor, master_name

router = APIRouter()

ac_query_trait = """
    MATCH
        (n:Gwas)-[oc:OBS_COR]-(m:Gwas)
    RETURN DISTINCT
        n.trait AS name
    """.replace(
    "\n", " "
)
ac_index_trait = "ac_obs_cor_trait"


@router.get("/obs-cor", response_model=bool)
def get_obs_cor(
    trait: str,
    cor_coef_threshold: float = Query(0.8, ge=-1.0, le=1.0),
    overwrite: bool = False,
) -> bool:
    """This is the master processor. For actual data use sub-apis"""
    log_args(api="/obs-cor", kwargs=locals())
    processor = ObsCorQueryProcessor(
        params={"trait": trait, "cor_coef_threshold": cor_coef_threshold}
    )
    res = processor.process_master(overwrite=overwrite)
    return res


@router.get(
    "/obs-cor/{endpoint}", response_model=models.standard_endpoint_response
)
def get_obs_cor_endpoints(
    endpoint: models.TopicViewEndpoints,
    trait: str,
    cor_coef_threshold: float = Query(0.8, ge=-1.0, le=1.0),
    rels_limit: int = rels_limit,
    overwrite: bool = False,
):
    log_args(api=f"/obs-cor/{endpoint.value}", kwargs=locals())
    processor = ObsCorQueryProcessor(
        params={"trait": trait, "cor_coef_threshold": cor_coef_threshold}
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


@router.get("/obs-cor/cache/drop", response_model=bool)
def get_obs_cor_cache_drop() -> bool:
    return mongo_cache_drop(master_name=master_name)


@router.get("/obs-cor/ac/index", response_model=bool)
def get_obs_cor_ac_index(overwrite: bool = False) -> bool:
    log_args(api="/obs-cor/ac/index", kwargs=locals())
    return index_ac_name_from_cypher(
        cypher_query=ac_query_trait,
        index_name=ac_index_trait,
        es_client=es_client,
        overwrite=overwrite,
    )


@router.get("/obs-cor/ac/trait", response_model=List[str])
def get_obs_cor_ac_trait(query: str, size: int = 20) -> List[str]:
    log_args(api="/obs-cor/ac/trait", kwargs=locals())
    if not es_client.indices.exists(index=ac_index_trait):
        get_obs_cor_ac_index()
    res = query_ac_name(
        query=query, index_name=ac_index_trait, es_client=es_client, size=size
    )
    return res
