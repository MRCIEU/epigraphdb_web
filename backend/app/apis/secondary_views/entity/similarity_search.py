from typing import Dict, List, Optional, Tuple

import requests
from pydash import py_

from app import settings
from app.apis.util_routes.search.functions import (
    annotate_search_results,
    query_node_info,
)
from app.funcs.annotate_entity import annotate_meta_entity, annotate_node_id

from . import models


def entity_name_search(
    reference_meta_node: str, id: str, name: str, size: int = 50
) -> List[models.SearchEntityNoScore]:
    query = name
    if reference_meta_node == "LiteratureTriple":
        search_results = _literature_triple_name_query(
            id=id, name=name, size=size
        )
    else:
        search_results = query_node_info(
            query=query, meta_node=None, size=size
        )
    res = annotate_search_results(search_results)
    return res


def entity_neural_search(
    reference_meta_node: str, id: str, name: str, size: int = 50
) -> Optional[List[models.SearchEntityScore]]:
    if reference_meta_node == "LiteratureTriple":
        search_results = _literature_triple_neural_query(
            id=id, name=name, size=size
        )
    else:
        search_results = _neural_search_by_id(
            id=id, meta_node=reference_meta_node, size=size
        )
    res: List[models.SearchEntityScore] = [
        {
            "id": annotate_node_id(_["id"], _["meta_node"]),
            "name": _["name"],
            "meta_node": annotate_meta_entity(_["meta_node"], "meta_node"),
            "score": _["score"],
        }
        for _ in search_results
    ]
    return res


def _literature_triple_name_query(
    id: str, name: str, size: int = 50
) -> List[Dict]:
    subject_term, object_term = _literature_triple_term_split(id, name)
    subject_results = query_node_info(
        query=subject_term, meta_node=None, size=int(size / 2)
    )
    object_results = query_node_info(
        query=object_term, meta_node=None, size=int(size / 2)
    )
    # TODO: should add ES score to alt version of query_node_info
    # then sort based on score
    res = subject_results + object_results
    return res


def _literature_triple_neural_query(
    id: str, name: str, size: int = 50
) -> List[Dict]:
    subject_term, object_term = _literature_triple_term_split(id, name)
    subject_results = _neural_search_by_text(
        text=subject_term, size=int(size / 2)
    )
    object_results = _neural_search_by_text(
        text=object_term, size=int(size / 2)
    )
    res = py_.sort(
        subject_results + object_results,
        key=lambda item: item["score"],
        reverse=True,
    )
    return res


def _neural_search_by_id(id: str, meta_node: str, size: int) -> List[Dict]:
    url = "{url}/query/entity".format(url=settings.neural_url)
    r = requests.get(
        url, params={"entity_id": id, "meta_node": meta_node, "limit": size}
    )
    r.raise_for_status()
    res: List[Dict] = r.json()
    return res


def _neural_search_by_text(text: str, size: int) -> List[Dict]:
    url = "{url}/query/text".format(url=settings.neural_url)
    r = requests.get(url, params={"text": text, "limit": size})
    r.raise_for_status()
    res: List[Dict] = r.json()["results"]
    return res


def _literature_triple_term_split(id: str, name: str) -> Tuple[str, str]:
    # literature triple: X PRED Y
    predicate = id.split(":")[1]
    terms = name.split(predicate)
    subject_term = terms[0].strip()
    object_term = terms[1].strip()
    res = (subject_term, object_term)
    return res
