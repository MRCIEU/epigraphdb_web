from typing import Any, Dict, List, Optional

import requests
from fastapi import APIRouter, HTTPException, Query

from app.apis.mr_simple.functions import (
    cypher_diagram,
    get_mr_simple_data,
    network_plot,
)
from app.settings import api_key, api_url
from app.utils.logging import log_args

router = APIRouter()


def validate_input(params: Dict[str, Any]):
    if params["exposure_trait"] is None and params["outcome_trait"] is None:
        raise HTTPException(
            status_code=422,
            detail="exposure and outcome can't be both missing.",
        )


@router.get("/mr-simple")
def get_mr_simple(
    exposure_trait: Optional[str] = None,
    outcome_trait: Optional[str] = None,
    pval_threshold: float = Query(1e-5, ge=0.0, le=1.0),
    rels_limit: int = 500,
):
    log_args(api="/mr-simple", kwargs=locals())
    validate_input(locals())
    # get response data, and process query
    table_df, empty_results, query_data = get_mr_simple_data(
        exposure_trait=exposure_trait,
        outcome_trait=outcome_trait,
        pval_threshold=pval_threshold,
    )
    # process diagram
    diagram_data = cypher_diagram(
        exposure_trait=exposure_trait,
        outcome_trait=outcome_trait,
        pval_threshold=pval_threshold,
    )
    if not empty_results:
        # process network plot
        network_plot_data = network_plot(
            table_df=table_df, rels_limit=rels_limit
        )
    else:
        network_plot_data = None
    table_data = (
        table_df.to_dict(orient="records") if table_df is not None else None
    )
    res = {
        "table_data": table_data,
        "network_plot_data": network_plot_data,
        "diagram_data": diagram_data,
        "query_data": query_data,
        "empty_results": empty_results,
    }
    return res


@router.get("/mr-simple/ac/trait", response_model=List[str])
def get_mr_simple_ac_trait():
    # NOTE: this is a naive implementation,
    #       to make it quick either limit the length of items returned
    #       or have some kind of caching.
    ac_query_trait = """
        MATCH
            (n:Gwas)-[r:MR]-(m:Gwas)
        WHERE
            r.pval < 0.1
        RETURN DISTINCT
            n.trait AS name
        LIMIT 500
        """.replace(
        "\n", " "
    )
    url = f"{api_url}/raw_cypher"
    r = requests.get(
        url=url, params={"query": ac_query_trait, "api_key": api_key}
    )
    r.raise_for_status()
    res = [_["name"] for _ in r.json()["results"]]
    return res
