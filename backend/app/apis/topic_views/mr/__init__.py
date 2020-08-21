from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query

from app import models
from app.funcs.elasticsearch.autocomplete import index_ac_name_from_cypher
from app.funcs.elasticsearch.query import query_ac_name
from app.utils.database import es_client, mongo_cache_drop
from app.utils.logging import log_args
from app.utils.queries import ac_mr_trait
from app.utils.visjs_config import rels_limit

from .functions import MRQueryProcessor, master_name

router = APIRouter()


def validate_input(params: Dict[str, Any]):
    if params["exposure_trait"] is None and params["outcome_trait"] is None:
        raise HTTPException(
            status_code=422,
            detail="exposure and outcome can't be both missing.",
        )


@router.get("/mr", response_model=bool)
def get_mr(
    exposure_trait: Optional[str] = None,
    outcome_trait: Optional[str] = None,
    pval_threshold: float = Query(1e-5, ge=0.0, le=1.0),
    overwrite: bool = False,
) -> bool:
    """This is the master processor. For actual data use sub-apis
    """
    log_args(api="/mr", kwargs=locals())
    validate_input(locals())
    processor = MRQueryProcessor(
        params={
            "exposure_trait": exposure_trait,
            "outcome_trait": outcome_trait,
            "pval_threshold": pval_threshold,
        }
    )
    res = processor.process_master(overwrite=overwrite)
    return res


@router.get("/mr/{endpoint}", response_model=models.standard_endpoint_response)
def get_mr_endpoints(
    endpoint: models.TopicViewEndpoints,
    exposure_trait: Optional[str] = None,
    outcome_trait: Optional[str] = None,
    pval_threshold: float = Query(1e-5, ge=0.0, le=1.0),
    rels_limit: int = rels_limit,
    overwrite: bool = False,
):
    log_args(api=f"/mr/{endpoint.value}", kwargs=locals())
    validate_input(locals())
    processor = MRQueryProcessor(
        params={
            "exposure_trait": exposure_trait,
            "outcome_trait": outcome_trait,
            "pval_threshold": pval_threshold,
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


@router.get("/mr/cache/drop", response_model=bool)
def get_mr_cache_drop() -> bool:
    return mongo_cache_drop(master_name=master_name)


@router.get("/mr/ac/index", response_model=bool)
def get_mr_ac_index(overwrite: bool = False) -> bool:
    log_args(api="/mr/ac/index", kwargs=locals())
    return index_ac_name_from_cypher(
        cypher_query=ac_mr_trait["query"],
        index_name=ac_mr_trait["index_name"],
        es_client=es_client,
        overwrite=overwrite,
    )


@router.get("/mr/ac/trait", response_model=List[str])
def get_mr_ac_trait(query: str, size: int = 20) -> List[str]:
    log_args(api="/mr/ac/trait", kwargs=locals())
    if not es_client.indices.exists(index=ac_mr_trait["index_name"]):
        get_mr_ac_index()
    res = query_ac_name(
        query=query,
        index_name=ac_mr_trait["index_name"],
        es_client=es_client,
        size=size,
    )
    return res
