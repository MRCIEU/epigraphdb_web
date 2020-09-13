from typing import Any, Dict

from app.funcs.cypher_diagram import CypherDiagram, DiagramEdge, DiagramNode
from app.funcs.query_processors import (
    NetworkPlotSchemaInput,
    TopicQueryProcessor,
)
from app.utils.data_table import NodeCol, RelCol

from .graph import edge_schemas, node_schemas

master_name = "drugs_risk_factors"
api_endpoint = "drugs/risk-factors"
TRAIT_DESC = ""
ASSOC_TRAIT_DESC = ""
DRUG_DESC = ""
GENE_DESC = ""
MR_DESC = ""
VARIANT_DESC = ""
table_col_configs = {
    "assoc_trait.id": NodeCol("Gwas", "id", ASSOC_TRAIT_DESC),
    "assoc_trait.trait": NodeCol("Gwas", "trait", ASSOC_TRAIT_DESC),
    "drug.label": NodeCol("Drug", "label", DRUG_DESC),
    "gene.name": NodeCol("Gene", "name", GENE_DESC),
    "mr.b": RelCol("MR", "b", MR_DESC, rounding=True),
    "mr.se": RelCol("MR", "se", MR_DESC, rounding=True),
    "mr.pval": RelCol("MR", "pval", MR_DESC),
    "mr.method": RelCol("MR", "method", MR_DESC),
    "mr.moescore": RelCol("MR", "moescore", MR_DESC),
    "mr.selection": RelCol("MR", "selection", MR_DESC),
    "variant.name": NodeCol("Variant", "name", VARIANT_DESC),
    "trait.id": NodeCol("Gwas", "id", TRAIT_DESC),
    "trait.trait": NodeCol("Gwas", "trait", TRAIT_DESC),
}


class DrugsRiskFactorsQueryProcessor(TopicQueryProcessor):
    def __init__(self, params: Dict[str, Any]):
        super().__init__(
            master_name=master_name,
            params=params,
            table_col_configs=table_col_configs,
            network_plot_schema=NetworkPlotSchemaInput(
                node_schemas=node_schemas, edge_schemas=edge_schemas
            ),
            cypher_diagram_fn=cypher_diagram,
            api_endpoint=api_endpoint,
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
