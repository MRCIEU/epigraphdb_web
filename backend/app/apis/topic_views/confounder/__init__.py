from enum import Enum
from typing import List, Union

from fastapi import APIRouter, Query

from app import models
from app.funcs.elasticsearch.autocomplete import index_ac_name_from_cypher
from app.funcs.elasticsearch.query import query_ac_name
from app.utils.database import es_client, mongo_cache_drop
from app.utils.logging import log_args
from app.utils.queries import ac_mr_trait
from app.utils.visjs_config import rels_limit

from .diagram import cypher_diagram
from .functions import ConfounderQueryProcessor, master_name

router = APIRouter()


class ConfounderType(str, Enum):
    confounder = "confounder"
    intermediate = "intermediate"
    reverse_intermediate = "reverse_intermediate"
    collider = "collider"


@router.get("/confounder", response_model=bool)
def get_confounder(
    exposure_trait: str,
    outcome_trait: str,
    confounder_type: ConfounderType = ConfounderType.confounder,
    pval_threshold: float = Query(1e-5, ge=0.0, le=1.0),
    overwrite: bool = False,
) -> bool:
    """This is the master processor. For actual data use sub-apis
    """
    log_args(api="/confounder", kwargs=locals())
    processor = ConfounderQueryProcessor(
        params={
            "exposure_trait": exposure_trait,
            "outcome_trait": outcome_trait,
            "type": confounder_type.value,
            "pval_threshold": pval_threshold,
        },
        type=confounder_type.value,
    )
    res = processor.process_master(overwrite=overwrite)
    return res


@router.get(
    "/confounder/{endpoint}",
    response_model=Union[
        None,
        models.TableDataResponse,
        models.GraphDataResponse,
        models.QueryDataResponse,
        models.DiagramResponse,
    ],
)
def get_confounder_endpoints(
    endpoint: models.TopicViewEndpoints,
    exposure_trait: str,
    outcome_trait: str,
    confounder_type: ConfounderType = ConfounderType.confounder,
    pval_threshold: float = Query(1e-5, ge=0.0, le=1.0),
    rels_limit: int = rels_limit,
    overwrite: bool = False,
):
    log_args(api=f"/confounder/{endpoint}", kwargs=locals())
    processor = ConfounderQueryProcessor(
        params={
            "exposure_trait": exposure_trait,
            "outcome_trait": outcome_trait,
            "type": confounder_type.value,
            "pval_threshold": pval_threshold,
        },
        type=confounder_type.value,
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


@router.get("/confounder/cache/drop", response_model=bool)
def get_confounder_cache_drop() -> bool:
    return mongo_cache_drop(master_name=master_name)


@router.get(
    "/confounder/query-diagram/plain/{confounder_type}",
    response_model=models.DiagramResponse,
)
def get_confounder_query_diagram_plain(
    confounder_type: ConfounderType = ConfounderType.confounder,
):
    """The plain version used in the frontend documentation
    """
    log_args(
        api=f"/confounder/query-diagram/plain/{confounder_type}",
        kwargs=locals(),
    )
    res = cypher_diagram(
        exposure_trait=None,
        outcome_trait=None,
        type=confounder_type,
        pval_threshold=None,
    )
    return res


@router.get("/confounder/ac/index", response_model=bool)
def get_confounder_ac_index(overwrite: bool = False) -> bool:
    log_args(api="/confounder/ac/index", kwargs=locals())
    return index_ac_name_from_cypher(
        cypher_query=ac_mr_trait["query"],
        index_name=ac_mr_trait["index_name"],
        es_client=es_client,
        overwrite=overwrite,
    )


@router.get("/confounder/ac/trait", response_model=List[str])
def get_confounder_ac_trait(query: str, size: int = 20) -> List[str]:
    log_args(api="/confounder/ac/trait", kwargs=locals())
    if not es_client.indices.exists(index=ac_mr_trait["index_name"]):
        get_confounder_ac_index()
    res = query_ac_name(
        query=query,
        index_name=ac_mr_trait["index_name"],
        es_client=es_client,
        size=size,
    )
    return res
