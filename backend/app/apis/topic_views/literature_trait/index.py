from app.funcs.elasticsearch.autocomplete import index_ac_name_from_cypher
from app.funcs.elasticsearch.indexers import (
    name_indexer_edge_ngram_long,
    name_indexer_edge_ngram_short,
)
from app.funcs.elasticsearch.query import query_ac_name
from app.utils.database import es_client
from app.utils.queries import ac_non_coding_trait

ac_configs = {
    "trait": {
        "index_name": ac_non_coding_trait["index_name"],
        "indexer_fn": name_indexer_edge_ngram_long,
        "query_fn": query_ac_name,
        "query": ac_non_coding_trait["query"],
    },
    "semmed_predicate": {
        "index_name": "ac_literature_trait_semmed_predicate",
        "indexer_fn": name_indexer_edge_ngram_short,
        "query_fn": query_ac_name,
        "query": """
            MATCH
                (triple:LiteratureTriple)
            RETURN DISTINCT
                triple.predicate AS name
            """.replace(
            "\n", " "
        ),
    },
}


def literature_trait_index_name(overwrite: bool = False) -> bool:
    index_res = [
        index_ac_name_from_cypher(
            cypher_query=configs["query"],
            index_name=configs["index_name"],
            es_client=es_client,
            indexer_fn=configs["indexer_fn"],
            overwrite=overwrite,
        )
        for name, configs in ac_configs.items()
    ]
    res = sum(index_res) == len(index_res)
    return res
