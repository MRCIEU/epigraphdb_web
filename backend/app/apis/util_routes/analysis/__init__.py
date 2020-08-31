from typing import Optional

import pandas as pd
import requests
from fastapi import APIRouter

from app.models import EpigraphdbGraphsExtended
from app.settings import api_url
from app.utils import api_request_headers
from app.utils.logging import log_args

from .functions import generate_df_descriptive_stats

router = APIRouter()


@router.get("/analysis/descriptive-stats")
def get_desc_stats(
    query: str,
    db: EpigraphdbGraphsExtended = EpigraphdbGraphsExtended.epigraphdb,
    hostname: Optional[str] = None,
    bolt_port: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
):
    """Converts query response to a pandas df,
    then returns summary stats from df
    """
    log_args(api="/analysis/descriptive-status", kwargs=locals())

    url = f"{api_url}/raw_cypher/"
    r = requests.get(
        url,
        params={
            "query": query,
            "db": db.value,
            "hostname": hostname,
            "bolt_port": bolt_port,
            "user": user,
            "password": password,
        },
        headers=api_request_headers,
    )
    r.raise_for_status()

    df = pd.json_normalize(r.json()["results"])
    res = generate_df_descriptive_stats(df)
    print(res)
    return res
