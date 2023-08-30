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

MASTER_ROUTE = "sc_eqtl_mr"


@router.get(f"/{MASTER_ROUTE}/list/{{entity}}")
def list_ents(entity: models.Entity, overwrite: bool = False):
    log_args(api=f"/{MASTER_ROUTE}/list/{entity}", kwargs=locals())

    def _func(entity: str):
        r = requests.get(
            f"{api_url}/{MASTER_ROUTE}/list/{entity}",
            headers=api_request_headers,
        )
        r.raise_for_status()
        res = r.json()["results"]
        return res

    cache_res = cache_func_call(
        coll_name=MASTER_ROUTE,
        func=_func,
        params={"entity": entity.value},
        overwrite=overwrite,
    )
    return cache_res


@router.get(f"/{MASTER_ROUTE}/query/{{entity}}")
def query(
    entity: models.Entity,
    q: Optional[str] = None,
    pval_threshold: float = 1e-3,
):
    log_args(api=f"/{MASTER_ROUTE}/query/{entity}", kwargs=locals())
    params: Dict[str, Any] = {"q": q, "pval_threshold": pval_threshold}
    r = requests.get(
        f"{api_url}/{MASTER_ROUTE}/query/{entity.value}",
        params=params,
        headers=api_request_headers,
    )
    r.raise_for_status()
    data = r.json()["results"]
    res = process_data(data=data)
    return res
