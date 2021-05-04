from typing import Dict, List
from urllib.parse import quote

import pandas as pd
from fastapi import APIRouter
from starlette.responses import Response

from app.apis.util_routes.api import get_api_cypher
from app.funcs.cache import cache_func_call
from app.models import EpigraphdbGraphsExtended
from app.utils.logging import log_args

from .pqtl_main import pqtl_main
from .pqtl_models import (
    PQTLListTableResponse,
    PQTLMethod,
    PQTLOutcome,
    PQTLResponse,
    PQTLSearchType,
)
from .pqtl_utils import query_api_pqtl_list

router = APIRouter()


@router.get("/pqtl", response_model=PQTLResponse)
def get_pqtl(query: str, method: PQTLMethod, overwrite: bool = False):
    log_args(api="/pqtl", kwargs=locals())
    exposure_proteins = get_pqtl_list(search_type=PQTLSearchType.exposures)
    outcome_traits = get_pqtl_list(search_type=PQTLSearchType.outcomes)
    if query.upper() in exposure_proteins:
        search_flag = "proteins"
    else:
        search_flag = "traits"
    res = pqtl_main(
        query=query,
        method=method.value,
        search_flag=search_flag,
        overwrite=overwrite,
    )
    return res


@router.get("/pqtl/list", response_model=List[str])
def get_pqtl_list(
    search_type: PQTLSearchType, overwrite: bool = False
) -> List[str]:
    log_args(api=f"/pqtl/list/{search_type}", kwargs=locals())
    res = cache_func_call(
        coll_name="pqtl_list",
        doc_name=search_type.value,
        func=query_api_pqtl_list,
        params={"search_flag": search_type.value},
        overwrite=overwrite,
    )
    return res


@router.get("/pqtl/list/table", response_model=PQTLListTableResponse)
def get_pqtl_list_table(search_type: PQTLSearchType, overwrite: bool = False):
    log_args(api=f"/pqtl/list/{search_type}", kwargs=locals())
    items = get_pqtl_list(search_type=search_type, overwrite=overwrite)
    res = {
        "table_titles": [
            {
                "label": "Protein list"
                if search_type == "exposures"
                else "Trait list",
                "key": "item",
            }
        ],
        "table_data": [{"item": item} for item in items],
    }
    return res


@router.get("/pqtl/list/combined", response_model=List[str])
def get_pqtl_list_combined(overwrite: bool = False) -> List[str]:
    log_args(api="/pqtl/list/combined", kwargs=locals())
    exposure_proteins = get_pqtl_list(
        search_type=PQTLSearchType.exposures, overwrite=overwrite
    )
    outcome_traits = get_pqtl_list(
        search_type=PQTLSearchType.outcomes, overwrite=overwrite
    )
    res = exposure_proteins + outcome_traits
    return res


@router.get("/pqtl/download")
def get_pqtl_download(query: str, method: PQTLMethod):
    log_args(api="/pqtl/download", kwargs=locals())
    pqtl_res = get_pqtl(query=query, method=method)
    table_df = pd.DataFrame.from_records(
        pqtl_res["table_output"]["table_items"]
    )
    res = table_df.to_csv(index=False)
    query_text = quote(query)
    filename = f"pqtl_{query_text}_{method.value}.csv"
    headers = {
        "Access-Control-Expose-Headers": "content-disposition",
        "content-disposition": f"attachment; filename={filename}",
    }
    return Response(res, media_type="text/csv", headers=headers)


@router.get("/pqtl/list/outcome", response_model=List[PQTLOutcome])
def get_pqtl_list_outcome(overwrite: bool = False) -> List[Dict[str, str]]:
    log_args(api="/pqtl/list/outcome", kwargs=locals())
    query = "MATCH (o:Outcome) RETURN DISTINCT o.outID_mrbase AS mrbase_id, o.outID AS label"
    cache_res = cache_func_call(
        coll_name="pqtl_list_outcome",
        func=get_api_cypher,
        params={"query": query, "db": EpigraphdbGraphsExtended.pqtl},
        overwrite=overwrite,
    )
    res = cache_res["results"]
    return res
