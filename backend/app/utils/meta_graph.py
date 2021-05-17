from typing import Callable, Optional

import pandas as pd

from app.settings import docs_url

from . import color_palette
from .meta_node_config import meta_node_dict
from .meta_rel_config import meta_rel_dict

node_def_url = f"{docs_url}/graph-database/meta-nodes/"
rel_def_url = f"{docs_url}/graph-database/meta-relationships/"


def meta_node_doc_url(meta_node: str) -> str:
    url = "{node_def_url}#{meta_node}".format(
        node_def_url=node_def_url, meta_node=meta_node.lower()
    )
    return url


def meta_rel_doc_url(meta_rel: str) -> str:
    url = "{rel_def_url}#{meta_rel}".format(
        rel_def_url=rel_def_url, meta_rel=meta_rel.lower()
    )
    return url


def meta_node_explore_url(meta_node: str) -> str:
    url = "/meta-node/{meta_node}".format(meta_node=meta_node)
    return url


def meta_rel_explore_url(meta_rel: str) -> str:
    url = "/meta-relationship/{meta_rel}".format(meta_rel=meta_rel)
    return url


meta_node_def = (
    pd.DataFrame.from_dict(meta_node_dict, orient="index")
    # Fill orig column
    .assign(
        orig_node=lambda df: df.apply(
            lambda row: row.name
            if pd.isnull(row["orig_node"])
            else row["orig_node"],
            axis=1,
        )
    )
    .assign(shape="box")
    .assign(
        url=lambda df: df.apply(
            lambda row: meta_node_doc_url(meta_node=row.at["orig_node"]),
            axis=1,
        )
    )
    .assign(explore=lambda df: df["explore"].fillna(value=False))
)

meta_rel_def = pd.DataFrame.from_dict(meta_rel_dict, orient="index")

line_color_dict = {
    "color": color_palette["grey"]["400"],
    "hover": color_palette["red"]["400"],
}


def find_orig_node(meta_node: str) -> str:
    res = meta_node_def["orig_node"][meta_node]
    return res


def gwas_label_formatter(
    node_name: Optional[str] = "gwas",
    id_col: str = "id",
    trait_col: str = "trait",
) -> Callable:
    """Changed to just use "{trait}"

    ~~A convenient wrapper to format gwas label to be "{id}: {trait}"~~
    """
    if node_name is not None:
        func = lambda row: "{trait}".format(
            trait=row[f"{node_name}.{trait_col}"]
        )
    else:
        func = lambda row: "{trait}".format(trait=row[trait_col])
    return func


def mr_eve_title_formatter(
    exposure_id: str = "exposure.id",
    outcome_id: str = "outcome.id",
    estimate: str = "mr.b",
    se: str = "mr.se",
    p: str = "mr.pval",
    selection: str = "mr.selection",
    method: str = "mr.method",
):
    func = lambda row: """
        <b>exposure.id</b>: {exposure_id},
        <b>outcome.id</b>: {outcome_id}</br>
        <b>estimate</b>: {estimate:.2E},
        <b>se</b>: {se:.2E},
        <b>pval</b>: {p:.2E}
        <b>selection</b>: {selection},
        <b>method</b>: {method}
        """.format(
        exposure_id=row[exposure_id],
        outcome_id=row[outcome_id],
        estimate=row[estimate],
        se=row[se],
        p=row[p],
        selection=row[selection],
        method=row[method],
    )
    return func
