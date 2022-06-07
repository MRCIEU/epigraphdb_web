"""This is adapted from epigraphdb-asq."""
import pandas as pd
import requests

from app.settings import api_url

ENT_URL_TEMPLATE = (
    "https://epigraphdb.org/entity?meta_node={meta_ent}&id={ent_id}"
)


def _query(query: str, ent_id: str, ent_type: str) -> pd.DataFrame:
    url = "{url}/cypher".format(url=api_url)
    r = requests.post(url, json={"query": query})
    r.raise_for_status()
    results = r.json()["results"]
    if len(results) == 0:
        column_names = ["ent_id", "ent_term", "ent_url"]
        empty_df = pd.DataFrame(columns=column_names)
        return empty_df
    else:
        df = pd.json_normalize(results).assign(
            ref_ent_id=ent_id,
            ent_type=ent_type,
            ent_url=lambda df: df["ent_id"].apply(
                lambda ent_id: ENT_URL_TEMPLATE.format(
                    meta_ent="Efo", ent_id=ent_id
                )
            ),
        )
    return df


def get_efo_data(ent_id: str) -> pd.DataFrame:
    self_query = """
    MATCH (efo:Efo)
    WHERE efo._id = "{ent_id}"
    RETURN
        efo._id AS ent_id,
        efo._name AS ent_term
    LIMIT 10
    """.format(
        ent_id=ent_id
    )
    parents_query = """
    MATCH (parent:Efo)-[r:EFO_CHILD_OF]->(ref:Efo)
    WHERE ref._id = "{ent_id}"
    RETURN
        parent._id AS ent_id,
        parent._name AS ent_term
    LIMIT 10
    """.format(
        ent_id=ent_id
    )
    children_query = """
    MATCH (ref:Efo)-[r:EFO_CHILD_OF]->(child:Efo)
    WHERE ref._id = "{ent_id}"
    RETURN
        child._id AS ent_id,
        child._name AS ent_term
    LIMIT 10
    """.format(
        ent_id=ent_id
    )
    self_df = _query(self_query, ent_id=ent_id, ent_type="ontology_self")
    parents_df = _query(
        parents_query, ent_id=ent_id, ent_type="ontology_parent"
    )
    if len(parents_df) > 0:
        parent_ents = parents_df["ent_id"].drop_duplicates().tolist()
        origin_df = pd.concat(
            [get_efo_shortest_from_origin(ent_id=_) for _ in parent_ents]
        )
    else:
        origin_df = pd.DataFrame()
    children_df = _query(
        children_query, ent_id=ent_id, ent_type="ontology_child"
    )
    res = pd.concat([self_df, parents_df, origin_df, children_df])
    return res


def get_efo_shortest_from_origin(ent_id: str) -> pd.DataFrame:
    root_id = "http://www.ebi.ac.uk/efo/EFO_0000001"
    query = """
    MATCH
        (root:Efo {{_id: "{root_id}"}}),
        (ref:Efo {{_id: "{ent_id}"}}),
        p = shortestPath((root)-[:EFO_CHILD_OF*]->(ref))
    WITH p
    WHERE length(p) > 1
    RETURN p
    """.format(
        root_id=root_id, ent_id=ent_id
    )
    url = "{url}/cypher".format(url=api_url)
    r = requests.post(url, json={"query": query})
    r.raise_for_status()
    results = r.json()["results"]
    if len(results) == 0:
        column_names = ["ent_id", "ent_term", "ent_url"]
        empty_df = pd.DataFrame(columns=column_names)
        return empty_df
    else:
        raw_nodes = results[0]["p"]["_nodes"]
        nodes = [
            {
                "ent_id": raw_nodes[idx]["_id"],
                "ent_term": raw_nodes[idx]["_name"],
                "ref_ent_id": raw_nodes[(idx + 1)]["_id"],
            }
            for idx in range(len(raw_nodes) - 1)
        ]
        nodes_df = pd.DataFrame(nodes).assign(
            ent_type="ontology_ancestor",
            ent_url=lambda df: df["ent_id"].apply(
                lambda ent_id: ENT_URL_TEMPLATE.format(
                    meta_ent="Efo", ent_id=ent_id
                )
            ),
        )
        return nodes_df
