from typing import List, Union

from fastapi import APIRouter, Query

from app import models
from app.funcs.elasticsearch.autocomplete import index_ac_name_from_cypher
from app.funcs.elasticsearch.query import query_ac_name
from app.utils.database import es_client, mongo_cache_drop
from app.utils.logging import log_args
from app.utils.visjs_config import rels_limit

from .functions import PrsQueryProcessor, master_name

router = APIRouter()

ac_query_trait = """
    MATCH
        (n:Gwas)-[prs:PRS]-(m:Gwas)
    WHERE
        prs.p < 0.001
    RETURN DISTINCT
        n.trait AS name
    """.replace(
    "\n", " "
)
ac_index_trait = "ac_prs_trait"


@router.get("/prs", response_model=bool)
def get_prs(
    trait: str,
    pval_threshold: float = Query(1e-5, ge=0.0, le=1.0),
    overwrite: bool = False,
) -> bool:
    """This is the master processor. For actual data use sub-apis
    """
    log_args(api="/prs", kwargs=locals())
    processor = PrsQueryProcessor(
        params={"trait": trait, "pval_threshold": pval_threshold}
    )
    res = processor.process_master(overwrite=overwrite)
    return res


@router.get(
    "/prs/{endpoint}",
    response_model=Union[
        None,
        models.TableDataResponse,
        models.GraphDataResponse,
        models.QueryDataResponse,
        models.DiagramResponse,
    ],
)
def get_genetic_cor_endpoints(
    endpoint: models.TopicViewEndpoints,
    trait: str,
    pval_threshold: float = Query(1e-5, ge=0.0, le=1.0),
    rels_limit: int = rels_limit,
    overwrite: bool = False,
):
    log_args(api=f"/prs/{endpoint.value}", kwargs=locals())
    processor = PrsQueryProcessor(
        params={"trait": trait, "pval_threshold": pval_threshold}
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


@router.get("/prs/cache/drop", response_model=bool)
def get_prs_cache_drop() -> bool:
    return mongo_cache_drop(master_name=master_name)


@router.get("/prs/ac/index", response_model=bool)
def get_prs_ac_index(overwrite: bool = False) -> bool:
    log_args(api="/prs/ac/index", kwargs=locals())
    return index_ac_name_from_cypher(
        cypher_query=ac_query_trait,
        index_name=ac_index_trait,
        es_client=es_client,
        overwrite=overwrite,
    )


@router.get("/prs/ac/trait", response_model=List[str])
def get_prs_ac_trait(query: str, size: int = 20) -> List[str]:
    log_args(api="/prs/ac/trait", kwargs=locals())
    if not es_client.indices.exists(index=ac_index_trait):
        get_prs_ac_index()
    res = query_ac_name(
        query=query, index_name=ac_index_trait, es_client=es_client, size=size
    )
    return res
