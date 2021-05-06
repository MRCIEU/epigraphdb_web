from typing import List

from app.apis.util_routes.search.functions import (
    annotate_search_results,
    query_node_info,
)

from . import models


def entity_similarity_search(
    reference_meta_node: str, id: str, name: str, size: int = 50
) -> List[models.SearchEntity]:
    query = name
    if reference_meta_node == "LiteratureTriple":
        search_results = literature_triple_query(id=id, name=name, size=size)
    else:
        search_results = query_node_info(
            query=query, meta_node=None, size=size
        )
    res = annotate_search_results(search_results)
    return res


def literature_triple_query(id: str, name: str, size: int = 50):
    # literature triple: X PRED Y
    predicate = id.split(":")[1]
    terms = name.split(predicate)
    subject_results = query_node_info(
        query=terms[0].rstrip(), meta_node=None, size=int(size / 2)
    )
    object_results = query_node_info(
        query=terms[1].rstrip(), meta_node=None, size=int(size / 2)
    )
    res = subject_results + object_results
    return res
