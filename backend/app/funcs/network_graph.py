import textwrap
from dataclasses import dataclass
from typing import Any, Callable, List, Optional

import pandas as pd

from app.utils import hex_to_rgb
from app.utils.logging import logger  # noqa:F401
from app.utils.meta_graph import (
    color_palette,
    find_orig_node,
    line_color_dict,
    meta_node_def,
    meta_rel_def,
)
from app.utils.visjs_config import node_alpha, node_wrap, visjs_option


@dataclass
class NetworkNodeSchema:
    """
    - id_col: column as the identifier of the node
    - label_col: column as the label to show on the node
    - label_formatter: a function to display the label, will override
                       `label_col`
    - meta_node: a node type (meta node) that can be found from `meta_graph_def`
    - cols: columns that are used in the processing of `url_formatter` or
            `title_formatter`
    - url_formatter: a function that takes the row of the datafraem as the
                     argument to format a clickable url
    - hover_title_formatter: a function that takes the row of the dataframe as the
                             argument to format the hover title
    - match_node_by:
      ["id", "name", None], when `url_formatter` is not set,
      and `match_node_scheme` is not None, then when double click on the node,
      will redirect to the node search view using `id_col`,
      and how the node is searched is determined how `id_col` is treated:
      - "id": treat `id_col` as "id" and search by exact matching
      - "name": treat `id_col` as "name" and search by fuzzy matching
    """

    meta_node: str
    id_col: str
    label_col: Optional[str] = None
    label_formatter: Optional[Callable] = None
    cols: Optional[List[str]] = None
    url_formatter: Optional[Callable] = None
    hover_title_formatter: Optional[Callable] = None
    match_node_by: Optional[str] = "id"

    def __post_init__(self) -> None:
        if self.label_col is None:
            self.label_col = self.id_col
        if self.hover_title_formatter is None:
            self.hover_title_formatter = lambda row: """
            <b>{orig_node}</b>: {label}
            """.format(
                orig_node=find_orig_node(row["meta_node"]),
                label=row[self.label_col],
            )
        if self.url_formatter is None and self.match_node_by is not None:
            if self.match_node_by == "id":
                self.url_formatter = id_match_formatter
            elif self.match_node_by == "name":
                self.url_formatter = name_match_formatter


@dataclass
class NetworkEdgeSchema:
    """
    - from_col: column used as the identifier of the "from" node
    - to_col: column used as the identifier of the "to" node
    - cols: columns that are used in the processing the formatters
    - from_meta_node: a node type (meta node) that can be found frrom `meta_graph_def`
    - to_meta_node: a node type (meta node) that can be found frrom `meta_graph_def`
    - arrows: If true then arrows will be used
    - hover_title_formatter: a function that takes the row of the dataframe as the
                             argument to format the hover title
    """

    from_col: str
    to_col: str
    cols: Optional[List[str]] = None
    from_meta_node: Optional[str] = None
    to_meta_node: Optional[str] = None
    arrows: bool = True
    dashes: bool = False
    hover_title_formatter: Optional[Callable] = None
    meta_rel: Optional[str] = None


class NetworkGraph:
    def __init__(
        self,
        df: pd.DataFrame,
        node_schemas: List[NetworkNodeSchema],
        edge_schemas: List[NetworkEdgeSchema],
        limit: Optional[int] = 50,
        visjs_option=visjs_option,
    ):
        """"""
        self.num_paths_total = len(df)
        if limit is not None:
            df = df[:limit]
        self.num_paths_displayed = len(df)

        self.visjs_option = visjs_option

        self.node_schemas = node_schemas
        self.edge_schemas = edge_schemas

        self.nodes_df = nodes_df_from_schema(df, self.node_schemas)
        logger.info(f"nodes_df: \n {self.nodes_df.head()}")

        self.edges_df = edges_df_from_schema(
            df, self.nodes_df, self.edge_schemas
        )
        logger.info(f"edges_df: \n {self.edges_df.head()}")

        self.nodes = render_nodes(self.nodes_df)
        self.nodes_3d = render_nodes_3d(self.nodes_df)
        logger.info(f"nodes: \n {self.nodes[0:2]}")

        self.edges = render_edges(self.edges_df)
        self.edges_3d = render_edges_3d(self.edges_df)
        logger.info(f"edges: \n {self.edges[0:2]}")

    def to_visjs(self):
        self.graph_data = {
            "nodes": self.nodes,
            "edges": self.edges,
            "nodes_3d": self.nodes_3d,
            "edges_3d": self.edges_3d,
            "option": self.visjs_option,
            "num_paths_total": self.num_paths_total,
            "num_paths_displayed": self.num_paths_displayed,
        }
        return self.graph_data


def network_graph(
    df: pd.DataFrame,
    node_schemas: List[NetworkNodeSchema],
    edge_schemas: List[NetworkEdgeSchema],
    limit: Optional[int],
):
    "Create visjs graph from query data."
    graph = NetworkGraph(
        df=df,
        node_schemas=node_schemas,
        edge_schemas=edge_schemas,
        limit=limit,
    )
    visjs_graph = graph.to_visjs()
    return visjs_graph


def process_node(df: pd.DataFrame, schema: NetworkNodeSchema) -> pd.DataFrame:
    df = df.dropna(subset=[schema.id_col])
    df = df.assign(orig_id=lambda df: df[schema.id_col].astype(str))
    # Node label: label_formatter > label_col
    if schema.label_formatter is not None:
        df = df.assign(
            label=lambda df: df.apply(schema.label_formatter, axis=1)
        )
    else:
        df = df.assign(label=lambda df: df[schema.label_col].astype(str))
    df = df.assign(meta_node=schema.meta_node)
    if schema.hover_title_formatter is not None:
        df = df.assign(
            title=lambda df: df.apply(schema.hover_title_formatter, axis=1)
        )
    else:
        df = df.assign(title=None)
    if schema.url_formatter is not None:
        df = df.assign(url=lambda df: df.apply(schema.url_formatter, axis=1))
    else:
        df = df.assign(url=None)
    df = df[
        ["orig_id", "label", "meta_node", "title", "url"]
    ].drop_duplicates()
    return df


def process_edge(df: pd.DataFrame, schema: NetworkEdgeSchema) -> pd.DataFrame:
    if schema.cols is not None and schema.cols != []:
        subset_cols = list(set([schema.from_col, schema.to_col, *schema.cols]))
    else:
        subset_cols = [schema.from_col, schema.to_col]
    for col in subset_cols:
        if col not in df.columns:
            return pd.DataFrame(None)
    df = df.dropna(subset=subset_cols)
    if len(df) == 0:
        return df
    df = df.assign(
        from_orig_id=lambda df: df[schema.from_col].astype(str),
        to_orig_id=lambda df: df[schema.to_col].astype(str),
    ).assign(
        from_meta_node=schema.from_meta_node, to_meta_node=schema.to_meta_node
    )
    if schema.hover_title_formatter is not None:
        df = df.assign(
            title=lambda df: df.apply(schema.hover_title_formatter, axis=1)
        )
    else:
        df = df.assign(title=None)
    df = df[
        [
            "from_orig_id",
            "to_orig_id",
            "from_meta_node",
            "to_meta_node",
            "title",
        ]
    ].drop_duplicates()
    # Set up color, arrows, etc
    # If not meta rel defined, follow source meta node
    if schema.meta_rel in meta_rel_def.index:
        df = (
            df.assign(meta_rel=schema.meta_rel)
            .merge(
                meta_rel_def[["color", "arrows", "dashes"]],
                how="left",
                left_on="meta_rel",
                right_index=True,
            )
            .drop(columns=["meta_rel"])
        )
    else:
        df = df.assign(arrows=schema.arrows, dashes=schema.dashes).merge(
            meta_node_def[["bg"]].rename(columns={"bg": "color"}),
            how="left",
            left_on="from_meta_node",
            right_index=True,
        )
    return df


def nodes_df_from_schema(
    df: pd.DataFrame, schema_list: List[NetworkNodeSchema]
) -> pd.DataFrame:
    nodes_df = (
        pd.concat(
            [process_node(df, schema) for schema in schema_list], sort=False
        )
        .drop_duplicates()
        .reset_index(drop=True)
        # Turn id into 1-indexed as required by visjs
        .assign(id=lambda df: df["orig_id"].astype("category").cat.codes + 1)
        # Add meta node info
        .merge(
            meta_node_def[["bg", "fg", "shape"]],
            left_on="meta_node",
            right_index=True,
        )
    )
    return nodes_df


def edges_df_from_schema(
    df: pd.DataFrame,
    nodes_df: pd.DataFrame,
    schema_list: List[NetworkEdgeSchema],
) -> pd.DataFrame:
    edges_df = (
        pd.concat(
            [process_edge(df, schema) for schema in schema_list], sort=False
        )
        .merge(
            nodes_df.rename(
                columns={"id": "from", "orig_id": "from_orig_id"}
            ).loc[:, ["from", "from_orig_id"]],
            how="left",
        )
        .merge(
            nodes_df.rename(columns={"id": "to", "orig_id": "to_orig_id"}).loc[
                :, ["to", "to_orig_id"]
            ],
            how="left",
        )
    )
    return edges_df


def render_nodes(nodes_df: pd.DataFrame) -> List[Any]:
    """The final step in processing nodes.

    Create a json-like list of nodes from nodes_df.
    """
    nodes = nodes_df.apply(
        lambda df: {
            "id": df["id"],
            "label": textwrap.fill(df["label"], node_wrap),
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
            "shape": df["shape"],
            "font": {"color": df["fg"]},
        },
        axis=1,
    ).tolist()
    return nodes


def render_nodes_3d(nodes_df: pd.DataFrame) -> List[Any]:
    """The final step in processing nodes.

    Create a json-like list of nodes from nodes_df.
    """
    nodes = nodes_df.apply(
        lambda df: {
            "id": df["id"],
            "name": df["label"],
            "color": df["bg"],
            "url": df["url"],
        },
        axis=1,
    ).tolist()
    return nodes


def render_edges(edges_df: pd.DataFrame) -> List[Any]:
    """The final step in processing edges.

    Create a json-like list of nodes from edges_df.
    """
    edges = edges_df.apply(
        lambda df: {
            "from": df["from"],
            "to": df["to"],
            "arrows": {"to": df["arrows"]},
            "scaling": {"min": 0.2, "max": 5},
            "arrowStrikethrough": df["arrows"],
            "value": 1,
            "dashes": df["dashes"],
            "title": df["title"],
            "color": {"color": df["color"], "hover": line_color_dict["hover"]},
        },
        axis=1,
    ).tolist()
    return edges


def render_edges_3d(edges_df: pd.DataFrame) -> List[Any]:
    """The final step in processing edges.

    Create a json-like list of nodes from edges_df.
    """
    edges = edges_df.apply(
        lambda df: {
            "source": df["from"],
            "target": df["to"],
            "color": df["color"],
        },
        axis=1,
    ).tolist()
    return edges


def id_match_formatter(row: pd.Series) -> str:
    url = "/explore/?meta_node={meta_node}&id={id}".format(
        meta_node=find_orig_node(row["meta_node"]), id=row["orig_id"]
    )
    return url


def name_match_formatter(row: pd.Series) -> str:
    url = "/explore/?meta_node={meta_node}&name={name}".format(
        meta_node=find_orig_node(row["meta_node"]), name=row["orig_id"]
    )
    return url
