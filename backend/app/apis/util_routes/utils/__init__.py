from typing import List, Optional

from fastapi import APIRouter

from app.apis import topic_views
from app.apis.util_routes import search
from app.utils.database import es_client, mongo_epigraphdb_web
from app.utils.logging import logger

router = APIRouter()

ES_EXCLUDE_PREFIX = ["embeddings-", ".apm-", ".kibana_"]


@router.get("/utils/cache/list", response_model=List[str])
def get_utils_cache_list() -> List[str]:
    """Returns the currently available cache collections."""
    colls = mongo_epigraphdb_web.list_collection_names()
    res = sorted(colls)
    return res


@router.get("/utils/cache/drop", response_model=bool)
def get_utils_cache_drop(
    collection_name: Optional[str] = None, all: bool = False
) -> bool:
    """Drop a mongodb collection, or every collection."""
    all_coll_names = mongo_epigraphdb_web.list_collection_names()
    if collection_name is not None and not all:
        if collection_name in all_coll_names:
            mongo_epigraphdb_web[collection_name].drop()
        new_all_coll_names = mongo_epigraphdb_web.list_collection_names()
        res = collection_name not in new_all_coll_names
        return res
    else:
        for collection_name in all_coll_names:
            mongo_epigraphdb_web[collection_name].drop()
        return True


@router.get("/utils/es/list", response_model=List[str])
def list_es_indices() -> List[str]:
    """Returns the currently available ES indices."""
    es_indices: List[str] = list(es_client.indices.get_alias("*").keys())
    return es_indices


@router.get("/utils/es/drop", response_model=bool)
def get_utils_es_drop(
    index_name: Optional[str] = None,
    all: bool = False,
    with_exclude: bool = False,
) -> bool:
    """Purge elasticsearch indices.

    - When specified with an `index_name`, drop it if it is not in exclude it
    - When `all`, drop all indices except those in exclude list
    - When `all` and `with_exclude`, drop all indices including those
      in exclude it
    """
    es_indices = list_es_indices()
    if index_name is not None:
        if index_name not in es_indices or not _es_index_not_exclude(
            index_name
        ):
            return False
        else:
            es_client.indices.delete(index=index_name, ignore=[400, 404])
            res = index_name not in list_es_indices()
            return res
    elif all:
        if not with_exclude:
            es_indices_subset = [
                _ for _ in es_indices if _es_index_not_exclude(_)
            ]
            for index in es_indices_subset:
                es_client.indices.delete(index=index, ignore=[400, 404])
            es_indices_subset = [
                _ for _ in list_es_indices() if _es_index_not_exclude(_)
            ]
            return len(es_indices_subset) == 0
        else:
            for index in es_indices:
                es_client.indices.delete(index=index, ignore=[400, 404])
            return len(list_es_indices()) == 0
    else:
        return False


@router.get("/utils/es/index", response_model=bool)
def get_utils_es_index(overwrite: bool = False) -> bool:
    logger.info("Index search indices.")
    assert search.get_index_all(overwrite=overwrite)
    logger.info("Index topic autocomplete indices.")
    index_funcs = [
        topic_views.mr.get_mr_ac_index,
        topic_views.obs_cor.get_obs_cor_ac_index,
        topic_views.genetic_cor.get_genetic_cor_ac_index,
        topic_views.confounder.get_confounder_ac_index,
        topic_views.drugs_risk_factors.get_drugs_risk_factors_ac_index,
        topic_views.pathway.get_pathway_ac_index,
        topic_views.prs.get_prs_ac_index,
        topic_views.xqtl.get_xqtl_ac_index,
        topic_views.literature_trait.get_literature_trait_ac_index,
        topic_views.ontology_trait_disease.get_ontology_trait_disease_ac_index,
    ]
    for func in index_funcs:
        logger.info(f"Indexing {func}")
        assert func(overwrite=overwrite)
    return True


def _es_index_not_exclude(index: str) -> bool:
    res = sum([not index.startswith(_) for _ in ES_EXCLUDE_PREFIX]) == len(
        ES_EXCLUDE_PREFIX
    )
    return res
