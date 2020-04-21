from typing import List

from elasticsearch import Elasticsearch


def query_ac_name(
    query: str, index_name: str, es_client: Elasticsearch, size: int = 20
) -> List[str]:
    query_body = {
        "query": {
            "match": {
                "name": {"query": query, "operator": "and", "fuzziness": 2}
            }
        },
        "size": size,
    }
    es_res = es_client.search(index=index_name, body=query_body)
    res = [item["_source"]["name"] for item in es_res["hits"]["hits"]]
    return res


def query_ac_name_prefix(
    query: str, index_name: str, es_client: Elasticsearch, size: int = 20
) -> List[str]:
    query_body = {
        "query": {"prefix": {"name": {"value": query}}},
        "size": size,
    }
    es_res = es_client.search(index=index_name, body=query_body)
    res = [item["_source"]["name"] for item in es_res["hits"]["hits"]]
    return res
