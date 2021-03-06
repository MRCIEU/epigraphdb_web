from typing import Any, Dict, Optional

import requests
from fastapi import APIRouter

from app.funcs.cache import cache_func_call
from app.settings import api_url
from app.utils import api_request_headers
from app.utils.logging import log_args

from . import models
from .functions import process_data

router = APIRouter()


@router.get("/covid-19/ctda/list/{entity}")
def get_list_ctda(entity: models.CovidXqtlList, overwrite: bool = False):
    log_args(api=f"/covid-19/ctda/list/{entity}", kwargs=locals())

    def _func(entity: str):
        r = requests.get(
            f"{api_url}/covid-19/ctda/list/{entity}",
            headers=api_request_headers,
        )
        r.raise_for_status()
        res = r.json()["results"]
        return res

    cache_res = cache_func_call(
        coll_name="covid_xqtl_list",
        func=_func,
        params={"entity": entity.value},
        overwrite=overwrite,
    )
    return cache_res


@router.get("/covid-19/ctda/single-snp-mr/{entity}")
def get_single_snp_mr(
    entity: models.CovidXqtlSingleSnpMrEntity,
    q: Optional[str] = None,
    pval_threshold: float = 1e-3,
):
    log_args(api=f"/covid-19/ctda/single-snp-mr/{entity}", kwargs=locals())
    params: Dict[str, Any] = {"q": q, "pval_threshold": pval_threshold}
    r = requests.get(
        f"{api_url}/covid-19/ctda/single-snp-mr/{entity.value}",
        params=params,
        headers=api_request_headers,
    )
    r.raise_for_status()
    data = r.json()["results"]
    res = process_data(data=data)
    return res


@router.get("/covid-19/ctda/multi-snp-mr/{entity}")
def get_multi_snp_mr(
    entity: models.CovidXqtlMultiSnpMrEntity,
    q: Optional[str] = None,
    pval_threshold: float = 1e-3,
):
    log_args(api=f"/covid-19/ctda/multi-snp-mr/{entity}", kwargs=locals())
    params: Dict[str, Any] = {"q": q, "pval_threshold": pval_threshold}
    r = requests.get(
        f"{api_url}/covid-19/ctda/multi-snp-mr/{entity.value}",
        params=params,
        headers=api_request_headers,
    )
    r.raise_for_status()
    data = r.json()["results"]
    res = process_data(data=data)
    return res
