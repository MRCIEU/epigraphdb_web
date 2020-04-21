"""Autocompletion functionality of epigraphdb entities
"""
from typing import Any, Callable, List

import requests
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from app.settings import api_key, api_url
from app.utils import batch_by_n
from app.utils.logging import logger

from .indexers import name_indexer_edge_ngram_long


def index_data(
    input_data: List[Any],
    index_name: str,
    es_client: Elasticsearch,
    indexer_fn: Callable,
    batch_size: int = 500,
    overwrite: bool = True,
) -> None:
    logger.info(f"Creating the index {index_name}.")
    indexer_fn(index_name=index_name, overwrite=overwrite, es_client=es_client)

    # NOTE: batch_data is a generator
    batch_data = batch_by_n(collection=input_data, batch_size=batch_size)
    for batch_docs in batch_data:
        requests = [
            dict(**{"_op_type": "index", "_index": index_name}, **doc)
            # {"_op_type": "index", "_index": index_name, "name": doc.name}
            for doc in batch_docs
        ]
        bulk(es_client, requests)

    es_client.indices.refresh(index=index_name, request_timeout=300)
    logger.info("Done indexing.")


def index_ac_name_from_cypher(
    cypher_query: str,
    index_name: str,
    es_client: Elasticsearch,
    indexer_fn: Callable = name_indexer_edge_ngram_long,
    overwrite: bool = False,
) -> bool:
    """Index entity names from upstream cypher query.

    Cypher results need to return a data structure like:
    [
       { "name": ... },
       { "name": ... },
    ]
    """
    if not es_client.indices.exists(index=index_name) or overwrite:
        cypher_url = f"{api_url}/raw_cypher/"
        r = requests.get(
            cypher_url, params={"query": cypher_query, "api_key": api_key}
        )
        r.raise_for_status()
        input_data = [dict(name=item["name"]) for item in r.json()["results"]]
        index_data(
            input_data=input_data,
            index_name=index_name,
            es_client=es_client,
            indexer_fn=indexer_fn,
        )
    return True
