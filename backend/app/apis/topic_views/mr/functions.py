from typing import Any, Dict, Optional

from app.funcs.cypher_diagram import CypherDiagram, DiagramEdge, DiagramNode
from app.funcs.query_processors import (
    NetworkPlotSchemaInput,
    TopicQueryProcessor,
)

from .graph import edge_schemas, node_schemas

master_name = "mr"
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


class MRQueryProcessor(TopicQueryProcessor):
    def __init__(self, params: Dict[str, Any]):
        super().__init__(
            master_name=master_name,
            params=params,
            table_cols=table_cols,
            network_plot_schema=NetworkPlotSchemaInput(
                node_schemas=node_schemas, edge_schemas=edge_schemas
            ),
            cypher_diagram_fn=cypher_diagram,
        )


def cypher_diagram(
    exposure_trait: Optional[str],
    outcome_trait: Optional[str],
    pval_threshold: float = 1e-5,
):
    """A diagram of cypher queries."""
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
            meta_rel="MR",
            sub_label=f"p < {pval_threshold}",
        )
    ]

    diagram = CypherDiagram(nodes=diagram_nodes, edges=diagram_edges)
    diagram_data = diagram.generate_diagram()
    return diagram_data
