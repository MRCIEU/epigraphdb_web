from typing import Any, Dict

from app.funcs.cypher_diagram import CypherDiagram, DiagramEdge, DiagramNode
from app.funcs.query_processors import (
    NetworkPlotSchemaInput,
    TopicQueryProcessor,
)

from .graph import edge_schemas, node_schemas

master_name = "drugs_risk_factors"
api_endpoint = "drugs/risk-factors"
table_cols = [
    "assoc_trait.id",
    "assoc_trait.trait",
    "drug.label",
    "gene.name",
    "mr.b",
    "mr.method",
    "mr.moescore",
    "mr.pval",
    "mr.se",
    "mr.selection",
    "variant.name",
    "trait.id",
    "trait.trait",
]
cols_to_round = ["mr.b", "mr.se", "mr.moescore"]


class DrugsRiskFactorsQueryProcessor(TopicQueryProcessor):
    def __init__(self, params: Dict[str, Any]):
        super().__init__(
            master_name=master_name,
            params=params,
            table_cols=table_cols,
            network_plot_schema=NetworkPlotSchemaInput(
                node_schemas=node_schemas, edge_schemas=edge_schemas
            ),
            cypher_diagram_fn=cypher_diagram,
            api_endpoint=api_endpoint,
            cols_to_round=cols_to_round,
        )


def cypher_diagram(trait: str, pval_threshold: float):
    diagram_nodes = [
        DiagramNode(id=1, meta_node="GwasExposure", label=f"Trait\n{trait}"),
        DiagramNode(id=2, meta_node="Gwas", label="Assoc_trait"),
        DiagramNode(id=3, meta_node="Variant"),
        DiagramNode(id=4, meta_node="Gene"),
        DiagramNode(id=5, meta_node="Drug"),
    ]
    diagram_edges = [
        DiagramEdge(
            from_id=2,
            to_id=1,
            meta_rel="MR",
            sub_label=f"\npval < {pval_threshold}"
            if pval_threshold is not None
            else "",
        ),
        DiagramEdge(
            from_id=2,
            to_id=3,
            meta_rel="GWAS_TO_VARIANT",
            sub_label="pval < 1e-8",
        ),
        DiagramEdge(from_id=4, to_id=3, meta_rel="VARIANT_TO_GENE"),
        DiagramEdge(from_id=5, to_id=4),
    ]
    diagram = CypherDiagram(nodes=diagram_nodes, edges=diagram_edges)
    diagram_data = diagram.generate_diagram()
    return diagram_data
