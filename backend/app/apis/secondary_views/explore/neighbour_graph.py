import textwrap

import pandas as pd

from app.funcs.network_graph import id_match_formatter
from app.models.meta_graph import epigraphdb_meta_nodes
from app.utils import hex_to_rgb
from app.utils.meta_graph import color_palette, line_color_dict, meta_node_def
from app.utils.visjs_config import node_alpha, node_wrap, visjs_option

# Number of nodes to be included in each of the meta group
neighbour_per_group_limit = 40


def neighbour_graph(graph_data):
    origin_df = pd.DataFrame(
        {
            "meta_node": [graph_data["meta_node"]],
            "orig_id": [graph_data["id"]],
            "node_name": [graph_data["id"]],
        }
    )
    neighbour_df = pd.DataFrame(
        [
            {
                "meta_node": item["meta_node"],
                "meta_rel": item["meta_rel"],
                "orig_id": node_item_get_orig_id(item),
                "node_name": node_item_get_name(item),
            }
            for item in graph_data["neighbour"]
            if item["meta_node"] in epigraphdb_meta_nodes.keys()
        ]
    )
    # When there are no suitable neighbours
    if len(neighbour_df) == 0:
        return None
    neighbour_df_subset = (
        neighbour_df.groupby("meta_node")
        .head(neighbour_per_group_limit)
        .reset_index(drop=True)
    )
    nodes_df = create_nodes_df(origin_df, neighbour_df_subset)
    edges_df = create_edges_df(origin_df, neighbour_df_subset, nodes_df)
    res = {
        "nodes": nodes_df_to_dict(nodes_df),
        "edges": edges_df_to_dict(edges_df),
        "nodes_3d": nodes_df_to_dict_3d(nodes_df),
        "edges_3d": edges_df_to_dict_3d(edges_df),
        "option": visjs_option,
    }
    return res


def node_item_get_orig_id(item):
    id_field = epigraphdb_meta_nodes[item["meta_node"]]["id"]
    # NOTE: We should always expect the node to contain the id field
    #       otherwise we should let it fail loudly
    return item["node_data"][id_field]


def node_item_get_name(item):
    name_field = epigraphdb_meta_nodes[item["meta_node"]]["name"]
    # If the expected name_field is not found in the node data,
    # use its id field instead
    if name_field in item["node_data"].keys():
        return item["node_data"][name_field]
    else:
        return node_item_get_orig_id(item)


def create_nodes_df(origin_df, neighbour_df_subset) -> pd.DataFrame:
    nodes_df = (
        pd.concat(
            [
                origin_df,
                neighbour_df_subset[["meta_node", "orig_id", "node_name"]],
            ]
        )
        .drop_duplicates()
        .reset_index(drop=True)
        .assign(shape="box")
        .assign(id=lambda df: df["orig_id"].astype("category").cat.codes + 1)
        .merge(
            meta_node_def[["bg", "fg"]], left_on="meta_node", right_index=True
        )
        .assign(
            title=lambda df: df.apply(
                lambda row: """
            <h4>{meta_node}</h4>
            <b>id</b>: {id}
            <b>name</b>: {name}
            """.format(
                    meta_node=row["meta_node"],
                    id=row["orig_id"],
                    name=row["node_name"],
                ),
                axis=1,
            )
        )
        .assign(url=lambda df: df.apply(id_match_formatter, axis=1))
        # .assign(url=None)
    )
    return nodes_df


def create_edges_df(
    origin_df: pd.DataFrame,
    neighbour_df_subset: pd.DataFrame,
    nodes_df: pd.DataFrame,
) -> pd.DataFrame:
    origin_id = origin_df["orig_id"][0]
    edges_df = (
        neighbour_df_subset[["meta_rel", "orig_id"]]
        .merge(
            nodes_df.rename(columns={"id": "to"})[["to", "orig_id"]],
            how="left",
            left_on="orig_id",
            right_on="orig_id",
        )
        .assign(
            title=lambda df: df.apply(
                lambda row: """
            <h4>{rel_name}</h4>
            """.format(
                    rel_name=row["meta_rel"]
                ),
                axis=1,
            )
        )
    )
    edges_df["from"] = nodes_df.loc[nodes_df["orig_id"] == origin_id, "id"][0]
    return edges_df


def nodes_df_to_dict(nodes_df):
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
            "shape": "box",
            "font": {"color": df["fg"]},
        },
        axis=1,
    ).tolist()
    return nodes_dict


def nodes_df_to_dict_3d(nodes_df):
    nodes_dict = nodes_df.apply(
        lambda df: {
            "id": df["id"],
            "name": df["node_name"],
            "color": df["bg"],
            "url": df["url"],
        },
        axis=1,
    ).tolist()
    return nodes_dict


def edges_df_to_dict(edges_df):
    edges_dict = edges_df.apply(
        lambda df: {
            "from": df["from"],
            "to": df["to"],
            "arrows": {"to": False},
            "arrowStrikethrough": False,
            "width": 2,
            "dashes": True,
            "title": df["title"],
            "color": {
                "color": line_color_dict["color"],
                "hover": line_color_dict["hover"],
            },
        },
        axis=1,
    ).tolist()
    return edges_dict


def edges_df_to_dict_3d(edges_df):
    edges_dict = edges_df.apply(
        lambda df: {
            "source": df["from"],
            "target": df["to"],
            "color": line_color_dict["color"],
        },
        axis=1,
    ).tolist()
    return edges_dict
