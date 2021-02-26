from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
import requests

from app.apis.mr_simple.graph import edge_schemas, node_schemas
from app.funcs.cypher_diagram import CypherDiagram, DiagramEdge, DiagramNode
from app.funcs.network_graph import network_graph
from app.funcs.render_query import render_query
from app.settings import api_url
from app.utils import api_request_headers
from app.utils.data_table import process_table_data

# remote API url endpoint
url = f"{api_url}/mr"
# names of columns to include in the table, and to determine order in the table
table_cols = [
    "exposure.id",
    "exposure.trait",
    "outcome.id",
    "outcome.trait",
    "mr.b",
    "mr.se",
    "mr.pval",
    "mr.method",
    "mr.selection",
    "mr.moescore",
]


def get_mr_simple_data(
    exposure_trait: Optional[str] = None,
    outcome_trait: Optional[str] = None,
    pval_threshold: float = 1e-5,
) -> Tuple[Optional[pd.DataFrame], bool, Dict[str, Any]]:
    """Handles the API requests, convert to table data, and associated query_data"""
    # NOTE: naming of param args is not always the same in API and Web
    params: Dict[str, Any] = {
        "exposure_trait": exposure_trait,
        "outcome_trait": outcome_trait,
        "pval_threshold": pval_threshold,
    }
    r = requests.get(url, params=params, headers=api_request_headers)
    # raise if status is not 200
    r.raise_for_status()
    response = r.json()
    results: List[object] = response["results"]
    # check if return data is empty
    empty_results = len(results) == 0
    # query_data: cypher statement, curl alternative, response preview, etc
    query_data = render_query(r=r, empty_results=empty_results)
    if not empty_results:
        # convert results to pandas df
        table_df = pd.json_normalize(results)[table_cols].pipe(
            process_table_data,
            cols_to_round=["mr.b", "mr.se", "mr.moescore"],
            to_dict=False,
        )
    else:
        table_df = None
    return table_df, empty_results, query_data


def network_plot(table_df: pd.DataFrame, rels_limit: int):
    """Convert table df into a visjs network plot"""
    network_plot_data = network_graph(
        df=table_df,
        node_schemas=node_schemas,
        edge_schemas=edge_schemas,
        limit=rels_limit,
    )
    return network_plot_data


def cypher_diagram(
    exposure_trait: Optional[str],
    outcome_trait: Optional[str],
    pval_threshold: float = 1e-5,
):
    """A diagram of cypher queries as a visjs network plot."""
    exposure_label = (
        f"exposure GWAS\n{exposure_trait}"
        if exposure_trait is not None
        else "exposure GWAS"
    )
    outcome_label = (
        f"outcome GWAS\n{outcome_trait}"
        if outcome_trait is not None
        else "outcome GWAS"
    )

    diagram_nodes = [
        DiagramNode(id=1, meta_node="Gwas", sub_label=exposure_label),
        DiagramNode(id=2, meta_node="Gwas", sub_label=outcome_label),
    ]
    diagram_edges = [
        DiagramEdge(
            from_id=1,
            to_id=2,
            meta_rel="MR_EVE_MR",
            sub_label=f"p < {pval_threshold}",
        )
    ]

    diagram = CypherDiagram(nodes=diagram_nodes, edges=diagram_edges)
    diagram_data = diagram.generate_diagram()
    return diagram_data
