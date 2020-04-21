from elasticsearch import Elasticsearch


def name_indexer_standard(
    index_name: str, es_client: Elasticsearch, overwrite: bool = True
) -> None:
    """Create an es index for autocompletion.

    Standard way, no use of edge ngram, used with prefix qeury
    """
    if overwrite:
        es_client.indices.delete(index=index_name, ignore=[404])
    request_body = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "refresh_interval": -1,
            "index.max_result_window": 100_000,
        },
        "mappings": {
            "dynamic": "true",
            "_source": {"enabled": "true"},
            "properties": {"name": {"type": "text"}},
        },
    }
    es_client.indices.create(
        index=index_name, body=request_body, request_timeout=60
    )


def name_indexer_edge_ngram_long(
    index_name: str, es_client: Elasticsearch, overwrite: bool = True
) -> None:
    """Create an es index for autocompletion using edge_ngram as tokenizer.

    Sources:
    - https://blog.mimacom.com/autocomplete-elasticsearch-part2/
    - https://www.elastic.co/guide/en/elasticsearch/reference/current/search-analyzer.html
    """
    if overwrite:
        es_client.indices.delete(index=index_name, ignore=[404])
    request_body = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "refresh_interval": -1,
            "index.max_result_window": 100_000,
            "analysis": {
                "analyzer": {
                    "autocomplete": {
                        "tokenizer": "autocomplete",
                        "filter": ["lowercase"],
                    },
                    "autocomplete_search": {"tokenizer": "lowercase"},
                },
                "tokenizer": {
                    "autocomplete": {
                        "type": "edge_ngram",
                        "min_gram": 3,
                        "max_gram": 10,
                        "token_chars": ["letter"],
                    }
                },
            },
        },
        "mappings": {
            "dynamic": "true",
            "_source": {"enabled": "true"},
            "properties": {
                "name": {
                    "type": "text",
                    "analyzer": "autocomplete",
                    "search_analyzer": "autocomplete_search",
                }
            },
        },
    }
    es_client.indices.create(
        index=index_name, body=request_body, request_timeout=60
    )


def name_indexer_edge_ngram_short(
    index_name: str, es_client: Elasticsearch, overwrite: bool = True
) -> None:
    """Create an es index for autocompletion using edge_ngram as tokenizer.

    For shorter names.
    """
    if overwrite:
        es_client.indices.delete(index=index_name, ignore=[404])
    request_body = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "refresh_interval": -1,
            "index.max_result_window": 100_000,
            "analysis": {
                "analyzer": {
                    "autocomplete": {
                        "tokenizer": "autocomplete",
                        "filter": ["lowercase"],
                    },
                    "autocomplete_search": {"tokenizer": "lowercase"},
                },
                "tokenizer": {
                    "autocomplete": {
                        "type": "edge_ngram",
                        "min_gram": 2,
                        "max_gram": 4,
                        "token_chars": [],
                    }
                },
            },
        },
        "mappings": {
            "dynamic": "true",
            "_source": {"enabled": "true"},
            "properties": {
                "name": {
                    "type": "text",
                    "analyzer": "autocomplete",
                    "search_analyzer": "autocomplete_search",
                }
            },
        },
    }
    es_client.indices.create(
        index=index_name, body=request_body, request_timeout=60
    )
