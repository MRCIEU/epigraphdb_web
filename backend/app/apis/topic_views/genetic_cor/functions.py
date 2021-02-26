from typing import Any, Dict

from app.funcs.cypher_diagram import CypherDiagram, DiagramEdge, DiagramNode
from app.funcs.query_processors import (
    NetworkPlotSchemaInput,
    TopicQueryProcessor,
)
from app.utils.data_table import NodeCol, RelCol
from app.utils.url_helpers import data_table_node_link, data_table_rel_link

from .graph import edge_schemas, node_schemas

master_name = "genetic-cor"
TRAIT_DESC = "{Gwas} trait of interests.".format(
    Gwas=data_table_node_link("Gwas")
)
ASSOC_TRAIT_DESC = "Associated {Gwas} trait.".format(
    Gwas=data_table_node_link("Gwas")
)
GC_DESC = "Genetic correlation ({GEN_COR}) between the two {Gwas} traits.".format(
    Gwas=data_table_node_link("Gwas"), GEN_COR=data_table_rel_link("GEN_COR")
)
table_col_configs = {
    "trait.id": NodeCol("Gwas", "id", TRAIT_DESC),
    "trait.trait": NodeCol("Gwas", "trait", TRAIT_DESC),
    "assoc_trait.id": NodeCol("Gwas", "id", ASSOC_TRAIT_DESC),
    "assoc_trait.trait": NodeCol("Gwas", "trait", ASSOC_TRAIT_DESC),
    "gc.rg": RelCol("GEN_COR", "rg", GC_DESC, rounding=True),
    "gc.rg_SE": RelCol("GEN_COR", "rg_SE", GC_DESC, rounding=True),
    "gc.Z": RelCol("GEN_COR", "Z", GC_DESC, rounding=True),
    "gc.p": RelCol("GEN_COR", "p", GC_DESC),
    "gc.rg_intercept": RelCol("GEN_COR", "rg_intercept", GC_DESC),
    "gc.rg_intercept_SE": RelCol("GEN_COR", "rg_intercept_SE", GC_DESC),
    "gc.h2": RelCol("GEN_COR", "h2", GC_DESC),
    "gc.h2_SE": RelCol("GEN_COR", "h2_SE", GC_DESC),
    "gc.h2_intercept": RelCol("GEN_COR", "h2_intercept", GC_DESC),
}


class GeneticCorQueryProcessor(TopicQueryProcessor):
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
            meta_rel="GEN_COR",
            sub_label=f"abs(gc.rg) > {cor_coef_threshold}",
            arrows=False,
        )
    ]

    diagram = CypherDiagram(nodes=diagram_nodes, edges=diagram_edges)
    diagram_data = diagram.generate_diagram()
    return diagram_data
