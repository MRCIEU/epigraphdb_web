from typing import Any, Dict, Optional

import requests

from app.settings import api_url
from app.utils.meta_graph import meta_node_doc_url

from .neighbour_graph import neighbour_graph

current_linked_resources = {
    "Gwas": {
        "url": "http://gwas.mrcieu.ac.uk/gwas/{id}/",
        "resource_name": "IEU Gwas Database",
        "logo": "igd-neg.svg",
    },
    "Literature": {
        "url": "https://www.ncbi.nlm.nih.gov/pubmed/{id}",
        "resource_name": "PubMed",
        "logo": "PubMed.png",
    },
}


def node_match(meta_node: str, id: Optional[str], name: Optional[str]):

    search_node_results = search_node(meta_node=meta_node, id=id, name=name)
    empty_results = True
    node_info = None
    if search_node_results is not None:
        empty_results = False
        search_neighbour_results = None
        neighbour_graph_data = None
        if id is not None:
            search_neighbour_results = search_neighbour(
                meta_node=meta_node, id=id
            )
            if search_neighbour_results is not None:
                neighbour_graph_data = neighbour_graph(
                    search_neighbour_results
                )

        node_info = {
            "results": search_node_results,
            "meta_node": meta_node,
            "id": id,
            "name": name,
            "neighbour_results": search_neighbour_results,
            "neighbour_graph_data": neighbour_graph_data,
            "doc_url": meta_node_doc_url(meta_node),
            "linked_resource": linked_resource(meta_node=meta_node, id=id),
        }
    res = {"node_info": node_info, "empty_results": empty_results}
    return res


def search_node(meta_node: str, id: Optional[str], name: Optional[str]):
    url = f"{api_url}/meta/nodes/{meta_node}/search"
    payload: Dict[str, Any] = {"id": id, "name": name}
    r = requests.get(url, params=payload)

    results = r.json()["results"]

    return results


def search_neighbour(meta_node: str, id: str):
    url = f"{api_url}/meta/nodes/{meta_node}/search-neighbour"
    payload = {"id": id}
    r = requests.get(url, params=payload)
    results = r.json()["results"]
    data = None
    if len(results) > 0:
        data = results[0]["data"]

    return data


def linked_resource(meta_node: str, id: Optional[str]):
    name: Optional[str]
    url: Optional[str]
    logo: Optional[str]
    if meta_node in current_linked_resources.keys() and id is not None:
        name = current_linked_resources[meta_node]["resource_name"]
        url = current_linked_resources[meta_node]["url"].format(id=id)
        logo = current_linked_resources[meta_node]["logo"]
    else:
        name = None
        url = None
        logo = None
    return {"name": name, "url": url, "logo": logo}
