from typing import Any, Dict

from app.funcs.cypher_diagram import CypherDiagram, DiagramEdge, DiagramNode
from app.funcs.query_processors import (
    NetworkPlotSchemaInput,
    TopicQueryProcessor,
)
from app.utils.data_table import NodeCol, RelCol
from app.utils.url_helpers import data_table_node_link, data_table_rel_link

from .graph import edge_schemas, node_schemas

master_name = "drugs_risk_factors"
api_endpoint = "drugs/risk-factors"
TRAIT_DESC = "Disease {Gwas} trait.".format(Gwas=data_table_node_link("Gwas"))
ASSOC_TRAIT_DESC = """
Risk factor {Gwas} trait that is identified to
have {MR_EVE_MR} evidence to the disease trait.
""".format(
    Gwas=data_table_node_link("Gwas"),
    MR_EVE_MR=data_table_rel_link("MR_EVE_MR"),
)
DRUG_DESC = """
{Drug} that is identified to be associated with the disease {Gwas} trait
via the path as shown in the network plot.
""".format(
    Gwas=data_table_node_link("Gwas"), Drug=data_table_node_link("Drug")
)
GENE_DESC = "Associated {Gene}".format(Gene=data_table_node_link("Gene"))
MR_DESC = """
Mendelian randomization {MR_EVE_MR} evidence
from the risk factor {Gwas} to the disease {Gwas}.
""".format(
    MR_EVE_MR=data_table_rel_link("MR_EVE_MR"),
    Gwas=data_table_node_link("Gwas"),
)
VARIANT_DESC = "Associated {Variant}".format(
    Variant=data_table_node_link("Variant")
)
table_col_configs = {
    "trait.id": NodeCol("Gwas", "id", TRAIT_DESC),
    "trait.trait": NodeCol("Gwas", "trait", TRAIT_DESC),
    "assoc_trait.id": NodeCol("Gwas", "id", ASSOC_TRAIT_DESC),
    "assoc_trait.trait": NodeCol("Gwas", "trait", ASSOC_TRAIT_DESC),
    "drug.label": NodeCol("Drug", "label", DRUG_DESC),
    "variant.name": NodeCol("Variant", "name", VARIANT_DESC),
    "gene.name": NodeCol("Gene", "name", GENE_DESC),
    "mr.b": RelCol("MR_EVE_MR", "b", MR_DESC, rounding=True),
    "mr.se": RelCol("MR_EVE_MR", "se", MR_DESC, rounding=True),
    "mr.pval": RelCol("MR_EVE_MR", "pval", MR_DESC),
    "mr.method": RelCol("MR_EVE_MR", "method", MR_DESC),
    "mr.moescore": RelCol("MR_EVE_MR", "moescore", MR_DESC),
    "mr.selection": RelCol("MR_EVE_MR", "selection", MR_DESC),
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
            meta_rel="MR_EVE_MR",
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
