from enum import Enum
from typing import List, Optional, Union

from fastapi import APIRouter

from app import models
from app.utils.database import es_client, mongo_cache_drop
from app.utils.logging import log_args
from app.utils.visjs_config import rels_limit

from .functions import LiteratureTraitQueryProcessor, master_name
from .index import ac_configs, literature_trait_index_name

router = APIRouter()


class LiteratureTraitAcIndex(str, Enum):
    trait = "trait"
    semmed_predicate = "semmed_predicate"


@router.get("/literature_trait", response_model=bool)
def get_literature_trait(
    trait: str,
    semmed_predicate: Optional[str],
    pval_threshold: float = 1e-5,
    overwrite: bool = False,
) -> bool:
    """This is the master processor. For actual data use sub-apis
    """
    log_args(api="/literature_trait", kwargs=locals())
    semmed_predicates = [semmed_predicate] if semmed_predicate is not None else None
    processor = LiteratureTraitQueryProcessor(
        params={
            "trait": trait,
            "semmed_predicates": semmed_predicates,
            "pval_threshold": pval_threshold,
        }
    )
    res = processor.process_master(overwrite=overwrite)
    return res


@router.get(
    "/literature_trait/{endpoint}",
    response_model=Union[
        None,
        models.TableDataResponse,
        models.GraphDataResponse,
        models.QueryDataResponse,
        models.DiagramResponse,
    ],
)
def get_literature_trait_endpoints(
    endpoint: models.TopicViewEndpoints,
    trait: str,
    semmed_predicate: Optional[str],
    pval_threshold: float = 1e-5,
    limit: int = 500,
    rels_limit: int = rels_limit,
    overwrite: bool = False,
):
    log_args(api=f"/literature_trait/{endpoint.value}", kwargs=locals())
    semmed_predicates = [semmed_predicate] if semmed_predicate is not None else None
    processor = LiteratureTraitQueryProcessor(
        params={
            "trait": trait,
            "semmed_predicates": semmed_predicates,
            "pval_threshold": pval_threshold,
            "limit": limit,
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


@router.get("/literature_trait/cache/drop", response_model=bool)
def get_literature_trait_cache_drop() -> bool:
    return mongo_cache_drop(master_name=master_name)


@router.get("/literature_trait/ac/index", response_model=bool)
def get_literature_trait_ac_index(overwrite: bool = False) -> bool:
    log_args(api="/literature_trait/ac/index", kwargs=locals())
    return literature_trait_index_name(overwrite=overwrite)


@router.get("/literature_trait/ac/{name}", response_model=List[str])
def get_literature_trait_ac(
    name: LiteratureTraitAcIndex, query: str, size: int = 20
) -> List[str]:
    log_args(api=f"/literature_trait/ac/{name}", kwargs=locals())
    ac_index = ac_configs[name.value]
    if not es_client.indices.exists(index=ac_index):
        get_literature_trait_ac_index()
    res = ac_configs[name]["query_fn"](
        query=query,
        index_name=ac_configs[name]["index_name"],
        es_client=es_client,
        size=size,
    )
    return res
