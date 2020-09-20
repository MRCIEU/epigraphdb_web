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
GC_DESC = "Genetic correlation ({BN_GEN_COR}) between the two {Gwas} traits.".format(
    Gwas=data_table_node_link("Gwas"),
    BN_GEN_COR=data_table_rel_link("BN_GEN_COR"),
)
table_col_configs = {
    "trait.id": NodeCol("Gwas", "id", TRAIT_DESC),
    "trait.trait": NodeCol("Gwas", "trait", TRAIT_DESC),
    "assoc_trait.id": NodeCol("Gwas", "id", ASSOC_TRAIT_DESC),
    "assoc_trait.trait": NodeCol("Gwas", "trait", ASSOC_TRAIT_DESC),
    "gc.rg": RelCol("BN_GEN_COR", "rg", GC_DESC, rounding=True),
    "gc.z": RelCol("BN_GEN_COR", "z", GC_DESC, rounding=True),
    "gc.se": RelCol("BN_GEN_COR", "se", GC_DESC, rounding=True),
    "gc.p": RelCol("BN_GEN_COR", "p", GC_DESC),
    "gc.h2_int": RelCol("BN_GEN_COR", "h2_int", GC_DESC, rounding=True),
    "gc.h2_int_se": RelCol("BN_GEN_COR", "h2_int_se", GC_DESC, rounding=True),
    "gc.h2_obs": RelCol("BN_GEN_COR", "h2_obs", GC_DESC),
    "gc.h2_obs_se": RelCol("BN_GEN_COR", "h2_obs_se", GC_DESC, rounding=True),
    "gc.gcov_int": RelCol("BN_GEN_COR", "gcov_int", GC_DESC, rounding=True),
    "gc.gcov_int_se": RelCol(
        "BN_GEN_COR", "gcov_int_se", GC_DESC, rounding=True
    ),
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
            meta_rel="BN_GEN_COR",
            sub_label=f"abs(gc.rg) > {cor_coef_threshold}",
            arrows=False,
        )
    ]

    diagram = CypherDiagram(nodes=diagram_nodes, edges=diagram_edges)
    diagram_data = diagram.generate_diagram()
    return diagram_data
