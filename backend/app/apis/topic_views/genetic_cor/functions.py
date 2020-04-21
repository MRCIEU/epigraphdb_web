from typing import Any, Dict

from app.funcs.cypher_diagram import CypherDiagram, DiagramEdge, DiagramNode
from app.funcs.query_processors import (
    NetworkPlotSchemaInput,
    TopicQueryProcessor,
)

from .graph import edge_schemas, node_schemas

master_name = "genetic-cor"
table_cols = [
    "trait.id",
    "trait.trait",
    "assoc_trait.id",
    "assoc_trait.trait",
    "gc.rg",
    "gc.z",
    "gc.se",
    "gc.p",
    "gc.h2_int",
    "gc.h2_int_se",
    "gc.h2_obs",
    "gc.h2_obs_se",
    "gc.gcov_int",
    "gc.gcov_int_se",
]


class GeneticCorQueryProcessor(TopicQueryProcessor):
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


def cypher_diagram(trait: str, cor_coef_threshold: float) -> str:
    """A diagram of cypher queries."""
    diagram_nodes = [
        DiagramNode(id=1, meta_node="Gwas", sub_label=trait),
        DiagramNode(id=2, meta_node="Gwas", sub_label="Associated trait"),
    ]
    diagram_edges = [
        DiagramEdge(
            from_id=1,
            to_id=2,
            meta_rel="BN_GEN_COR",
            sub_label=f"abs(gc.rg) > {cor_coef_threshold}",
            arrows=False,
        )
    ]

    diagram = CypherDiagram(nodes=diagram_nodes, edges=diagram_edges)
    diagram_data = diagram.generate_diagram()
    return diagram_data
