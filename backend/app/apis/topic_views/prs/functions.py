from typing import Any, Dict

from app.funcs.cypher_diagram import CypherDiagram, DiagramEdge, DiagramNode
from app.funcs.query_processors import (
    NetworkPlotSchemaInput,
    TopicQueryProcessor,
)
from app.utils.data_table import NodeCol, RelCol
from app.utils.url_helpers import data_table_node_link, data_table_rel_link

from .graph import edge_schemas, node_schemas

master_name = "prs"
TRAIT_DESC = "The {gwas} trait of interests.".format(
    gwas=data_table_node_link("Gwas")
)
ASSOC_TRAIT_DESC = "The associated {gwas} trait.".format(
    gwas=data_table_node_link("Gwas")
)

PRS_DESC = "Pre-computed polygenic risk scores {prs} associations.".format(
    prs=data_table_rel_link("PRS")
)
table_col_configs = {
    "trait.id": NodeCol("Gwas", "id", TRAIT_DESC),
    "trait.trait": NodeCol("Gwas", "trait", TRAIT_DESC),
    "assoc_trait.id": NodeCol("Gwas", "id", ASSOC_TRAIT_DESC),
    "assoc_trait.trait": NodeCol("Gwas", "trait", ASSOC_TRAIT_DESC),
    "prs.beta": RelCol("PRS", "beta", PRS_DESC, rounding=True),
    "prs.se": RelCol("PRS", "se", PRS_DESC, rounding=True),
    "prs.p": RelCol("PRS", "p", PRS_DESC),
    "prs.r2": RelCol("PRS", "r2", PRS_DESC, rounding=True),
    "prs.nsnps": RelCol("PRS", "nsnps", PRS_DESC),
    "prs.n": RelCol("PRS", "n", PRS_DESC),
    "prs.model": RelCol("PRS", "model", PRS_DESC),
}


class PrsQueryProcessor(TopicQueryProcessor):
    def __init__(self, params: Dict[str, Any]):
        super().__init__(
            master_name=master_name,
            params=params,
            table_col_configs=table_col_configs,
            network_plot_schema=NetworkPlotSchemaInput(
                node_schemas=node_schemas, edge_schemas=edge_schemas
            ),
            cypher_diagram_fn=cypher_diagram,
        )


def cypher_diagram(trait: str, pval_threshold: float) -> str:
    """A diagram of cypher queries."""
    diagram_nodes = [
        DiagramNode(id=1, meta_node="Gwas", sub_label=trait),
        DiagramNode(id=2, meta_node="Gwas", sub_label="Associated trait"),
    ]
    diagram_edges = [
        DiagramEdge(
            from_id=1,
            to_id=2,
            meta_rel="PRS",
            sub_label=f"pval < {pval_threshold}",
            arrows=False,
        )
    ]

    diagram = CypherDiagram(nodes=diagram_nodes, edges=diagram_edges)
    diagram_data = diagram.generate_diagram()
    return diagram_data
