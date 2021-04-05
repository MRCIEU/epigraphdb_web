from enum import Enum
from functools import reduce
from operator import mul
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query

from app import models
from app.utils.database import es_client, mongo_cache_drop
from app.utils.logging import log_args
from app.utils.visjs_config import rels_limit

from .functions import (
    XqtlQueryProcessor,
    multi_snp_master_name,
    single_snp_master_name,
)
from .index import ac_configs, xqtl_index_name

router = APIRouter()


class XqtlMode(str, Enum):
    multi_snp_mr = "multi_snp_mr"
    single_snp_mr = "single_snp_mr"


class XqtlMrMethod(str, Enum):
    ivw = "IVW"
    egger = "Egger"


class XqtlQtlType(str, Enum):
    eqtl = "eQTL"
    pqtl = "pQTL"


class XqtlAcIndex(str, Enum):
    exposure_gene = "exposure_gene"
    outcome_trait = "outcome_trait"
    variant = "variant"


def validate_input(params: Dict[str, Any]):
    if (
        params["exposure_gene"] is None
        and params["outcome_trait"] is None
        and params["variant"] is None
    ):
        raise HTTPException(
            status_code=422,
            detail="At least one of [exposure_gene, outcome_trait, variant] needs to exist",
        )


@router.get("/xqtl", response_model=bool)
def get_xqtl(
    xqtl_mode: XqtlMode = XqtlMode.multi_snp_mr,
    exposure_gene: Optional[str] = None,
    outcome_trait: Optional[str] = None,
    variant: Optional[str] = None,
    mr_method: XqtlMrMethod = XqtlMrMethod.ivw,
    qtl_type: XqtlQtlType = XqtlQtlType.eqtl,
    pval_threshold: float = Query(1e-5, ge=0.0, le=1.0),
    overwrite: bool = False,
) -> bool:
    """This is the master processor. For actual data use sub-apis"""
    log_args(api="/xqtl", kwargs=locals())
    validate_input(locals())
    processor = XqtlQueryProcessor(
        params={
            "xqtl_mode": xqtl_mode.value,
            "exposure_gene": exposure_gene,
            "outcome_trait": outcome_trait,
            "variant": variant,
            "mr_method": mr_method.value,
            "qtl_type": qtl_type.value,
            "pval_threshold": pval_threshold,
        }
    )
    res = processor.process_master(overwrite=overwrite)
    return res


@router.get(
    "/xqtl/{endpoint}", response_model=models.standard_endpoint_response
)
def get_xqtl_endpoints(
    endpoint: models.TopicViewEndpoints,
    xqtl_mode: XqtlMode = XqtlMode.multi_snp_mr,
    exposure_gene: Optional[str] = None,
    outcome_trait: Optional[str] = None,
    variant: Optional[str] = None,
    mr_method: XqtlMrMethod = XqtlMrMethod.ivw,
    qtl_type: XqtlQtlType = XqtlQtlType.eqtl,
    pval_threshold: float = Query(1e-5, ge=0.0, le=1.0),
    rels_limit: int = rels_limit,
    overwrite: bool = False,
):
    log_args(api=f"/xqtl/{endpoint.value}", kwargs=locals())
    validate_input(locals())
    processor = XqtlQueryProcessor(
        params={
            "xqtl_mode": xqtl_mode.value,
            "exposure_gene": exposure_gene,
            "outcome_trait": outcome_trait,
            "variant": variant,
            "mr_method": mr_method.value,
            "qtl_type": qtl_type.value,
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


@router.get("/xqtl/cache/drop", response_model=bool)
def get_xqtl_cache_drop() -> bool:
    # wtf there isn't a sum equivalent for multiply until py3.8
    res = reduce(
        mul,
        [
            mongo_cache_drop(master_name=single_snp_master_name),
            mongo_cache_drop(master_name=multi_snp_master_name),
        ],
    )
    return res


@router.get("/xqtl/ac/index", response_model=bool)
def get_xqtl_ac_index(overwrite: bool = False) -> bool:
    log_args(api="/xqtl/ac/index", kwargs=locals())
    return xqtl_index_name(overwrite=overwrite)


@router.get("/xqtl/ac/{name}", response_model=List[str])
def get_xqtl_ac(name: XqtlAcIndex, query: str, size: int = 20) -> List[str]:
    log_args(api=f"/xqtl/ac/{name}", kwargs=locals())
    ac_index = ac_configs[name.value]
    if not es_client.indices.exists(index=ac_index):
        get_xqtl_ac_index()
    res = ac_configs[name]["query_fn"](
        query=query,
        index_name=ac_configs[name]["index_name"],
        es_client=es_client,
        size=size,
    )
    return res
