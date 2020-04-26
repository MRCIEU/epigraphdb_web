import math
import textwrap
from itertools import chain

import numpy as np
import pandas as pd
import requests

from app.funcs.cache import cache_func_call
from app.settings import api_url
from app.utils import format_df_results, hex_to_rgb
from app.utils.meta_graph import (
    color_palette,
    line_color_dict,
    meta_node_def,
    rel_def_url,
)
from app.utils.visjs_config import node_alpha, node_wrap, visjs_option


def get_schema(overwrite: bool = False):
    nodes_data, edges_data = schema_request(overwrite=overwrite)
    nodes_df, rels_df, edges_df = process_nodes_edges(nodes_data, edges_data)
    graph = schema_graph(nodes_df, rels_df, edges_df)
    nodes = (
        nodes_df.rename(columns={"node_name": "node"})[["node", "count"]]
        .assign(count=lambda df: df["count"].apply(lambda x: f"{x:,}"))
        .pipe(format_df_results)
    )
    rels = (
        edges_df[["relationship", "count"]]
        .assign(count=lambda df: df["count"].apply(lambda x: f"{x:,}"))
        .pipe(format_df_results)
    )
    res = {"graph": graph, "nodes": nodes, "rels": rels}
    return res


def schema_request(overwrite: bool = False):
    def query_func():
        url = f"{api_url}/status/db"
        payload = {"metric": "schema", "db": "epigraphdb"}
        r = requests.get(url, params=payload)
        r.raise_for_status()
        res = r.json()[0]["value"]
        return res

    doc_name = "schema_data"
    coll_name = "schema"
    schema_data = cache_func_call(
        coll_name=coll_name,
        doc_name=doc_name,
        func=query_func,
        params=None,
        overwrite=overwrite,
    )

    nodes_data = {
        key: value
        for key, value in schema_data.items()
        if value["type"] == "node"
    }

    edges_data = {
        key: value
        for key, value in schema_data.items()
        if value["type"] == "relationship"
    }
    return nodes_data, edges_data


def process_nodes_edges(nodes_data, edges_data):
    # fmt: off
    nodes_df = pd.concat(
        map(lambda node_name, node: pd.DataFrame([{
            "node_name": node_name,
            "count": node["count"]
        }]),
            *zip(*nodes_data.items())),
        sort=False)
    edges_df = pd.concat(
        map(lambda rel_name, rel: pd.DataFrame([{
            "relationship": rel_name,
            "count": rel["count"]
        }]),
            *zip(*edges_data.items())),
        sort=False)
    # fmt:on

    # Filter `nodes_data` that have non-empty relationships
    nodes_data_for_rels = {
        key: value
        for key, value in nodes_data.items()
        if len(value["relationships"]) > 0
    }
    # fmt: off
    # Pluck a nested hierachical structure
    rels_df = pd.concat(
        chain.from_iterable(
            map(lambda node_name, node: map(
                lambda rel_name, rel: pd.DataFrame(
                    {
                        "relationship": rel_name,
                        "source_node": node_name,
                        "direction": rel["direction"],
                        "count": rel["count"],
                        "target_node": rel["labels"],
                    }
                ),
                *zip(*node["relationships"].items()),
            ),
                *zip(*nodes_data_for_rels.items()))))
    # fmt: on
    rels_df = (
        pd.concat(
            [
                rels_df[rels_df["direction"] == "out"].rename(
                    columns={
                        "source_node": "from_node",
                        "target_node": "to_node",
                    }
                ),
                rels_df[rels_df["direction"] == "in"].rename(
                    columns={
                        "source_node": "to_node",
                        "target_node": "from_node",
                    }
                ),
            ],
            sort=False,
        )
        .drop(columns="direction")
        .drop_duplicates()
        .reset_index(drop=True)
        .groupby(["from_node", "to_node", "relationship"])
        .sum()
        .reset_index()
    )
    return nodes_df, rels_df, edges_df


def schema_graph(nodes_df, rels_df, edges_df):
    # FIXME: should show node with default color when the node is not defined
    #        in the meta_graph
    nodes_df = (
        nodes_df.reset_index(drop=True)
        .replace({np.nan: None})
        .merge(meta_node_def, left_on="node_name", right_index=True)
        .assign(shape="box")
        .assign(id=lambda df: df["node_name"].astype("category").cat.codes + 1)
        .assign(
            title=lambda df: df.apply(
                lambda row: """
            <h4>{node_name}</h4>
            <b>count</b>: {count:,}
            """.format(
                    node_name=row["node_name"], count=row["count"]
                ),
                axis=1,
            )
        )
    )
    rels_df = (
        rels_df.replace({np.nan: None})
        .merge(
            nodes_df.rename(
                columns={"id": "from", "node_name": "from_node", "bg": "color"}
            )[["from", "from_node", "color"]],
            how="left",
        )
        .merge(
            nodes_df.rename(columns={"id": "to", "node_name": "to_node"})[
                ["to", "to_node"]
            ],
            how="left",
        )
        .merge(
            edges_df[["relationship", "count"]],
            # left_on="relationship",
            # right_on="relationship",
            how="left",
        )
        .assign(
            title=lambda df: df.apply(
                lambda row: """
            <h4>{rel_name}</h4>
            <b>count</b>: {count:,}
            """.format(
                    rel_name=row["relationship"], count=row["count"]
                ),
                axis=1,
            )
        )
        .assign(
            url=lambda df: df.apply(
                lambda row: "{rel_def_url}#{meta_rel}".format(
                    rel_def_url=rel_def_url,
                    meta_rel=row.at["relationship"].lower(),
                ),
                axis=1,
            )
        )
    )
    nodes_dict = nodes_df.apply(
        lambda df: {
            "id": df["id"],
            "label": textwrap.fill(df["node_name"], node_wrap),
            "title": df["title"],
            "url": df["url"],
            "color": {
                "background": hex_to_rgb(df["bg"], alpha=node_alpha),
                "highlight": {
                    "background": df["bg"],
                    "border": color_palette["red"]["600"],
                },
                "hover": {
                    "background": df["bg"],
                    "border": color_palette["red"]["600"],
                },
            },
            "shape": "circle",
            "font": {"color": df["fg"]},
        },
        axis=1,
    ).tolist()
    nodes_3d = nodes_df.apply(
        lambda df: {
            "id": df["id"],
            "name": df["node_name"],
            "color": df["bg"],
            "url": df["url"],
        },
        axis=1,
    ).tolist()
    rels_dict = rels_df.apply(
        lambda df: {
            "from": df["from"],
            "to": df["to"],
            "arrows": {"to": True},
            "scaling": {"min": 0.2, "max": 5},
            "arrowStrikethrough": True,
            "url": df["url"],
            "value": 1,
            "dashes": True,
            "title": df["title"],
            "color": {"color": df["color"], "hover": line_color_dict["hover"]},
        },
        axis=1,
    ).tolist()
    edges_3d = rels_df.apply(
        lambda df: {
            "source": df["from"],
            "target": df["to"],
            "color": df["color"],
            "curvature": np.random.uniform(0.1, 0.5),
            "rotation": np.random.uniform(0.5, math.pi),
        },
        axis=1,
    ).tolist()
    graph_data = {
        "nodes": nodes_dict,
        "edges": rels_dict,
        "nodes_3d": nodes_3d,
        "edges_3d": edges_3d,
        "option": visjs_option,
    }
    return graph_data
