from typing import Any, Dict

from app.funcs.cypher_diagram import CypherDiagram, DiagramEdge, DiagramNode
from app.funcs.query_processors import (
    NetworkPlotSchemaInput,
    TopicQueryProcessor,
)
from app.utils.data_table import NodeCol, RelCol
from app.utils.url_helpers import data_table_node_link, data_table_rel_link

from .graph import edge_schemas, node_schemas

master_name = "pathway"
GWAS_DESC = "{Gwas} trait of interests".format(
    Gwas=data_table_node_link("Gwas")
)
GWAS_TO_VARIANT_DESC = """
Identified association ({GWAS_TO_VARIANT}) between {Gwas} and {Variant}
""".format(
    GWAS_TO_VARIANT=data_table_rel_link("GWAS_TO_VARIANT"),
    Gwas=data_table_node_link("Gwas"),
    Variant=data_table_node_link("Variant"),
)
VARIANT_DESC = "Associated {Variant}".format(
    Variant=data_table_node_link("Variant")
)
GENE_DESC = "Associated {Gene}".format(Gene=data_table_node_link("Gene"))
PROTEIN_DESC = "Associated {Protein}".format(
    Protein=data_table_node_link("Protein")
)
PATHWAY_DESC = "Biological {Pathway}".format(
    Pathway=data_table_node_link("Pathway")
)
table_col_configs = {
    "gwas.id": NodeCol("Gwas", "id", GWAS_DESC),
    "gwas.trait": NodeCol("Gwas", "trait", GWAS_DESC),
    "gwas_to_variant.beta": RelCol(
        "GWAS_TO_VARIANT", "beta", GWAS_TO_VARIANT_DESC, rounding=True
    ),
    "gwas_to_variant.se": RelCol(
        "GWAS_TO_VARIANT", "se", GWAS_TO_VARIANT_DESC, rounding=True
    ),
    "gwas_to_variant.pval": RelCol(
        "GWAS_TO_VARIANT", "pval", GWAS_TO_VARIANT_DESC
    ),
    "gwas_to_variant.samplesize": RelCol(
        "GWAS_TO_VARIANT", "samplesize", GWAS_TO_VARIANT_DESC
    ),
    "variant.name": NodeCol("Variant", "name", VARIANT_DESC),
    "gene.name": NodeCol("Gene", "name", GENE_DESC),
    "protein.uniprot_id": NodeCol("Protein", "uniprot_id", PROTEIN_DESC),
    "pathway.id": NodeCol("Pathway", "id", PATHWAY_DESC),
    "pathway.name": NodeCol("Pathway", "name", PATHWAY_DESC),
}


class PathwayQueryProcessor(TopicQueryProcessor):
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


def cypher_diagram(trait: str, pval_threshold: float):
    diagram_nodes = [
        DiagramNode(id=1, meta_node="Gwas", sub_label=f"{trait}"),
        DiagramNode(id=2, meta_node="Variant"),
        DiagramNode(id=3, meta_node="Gene"),
        DiagramNode(id=4, meta_node="Protein"),
        DiagramNode(id=5, meta_node="Pathway"),
    ]
    diagram_edges = [
        DiagramEdge(
            from_id=1,
            to_id=2,
            meta_rel="GWAS_TO_VARIANT",
            sub_label=f"pval < {pval_threshold}"
            if pval_threshold is not None
            else "",
        ),
        DiagramEdge(from_id=2, to_id=3, meta_rel="VARIANT_TO_GENE"),
        DiagramEdge(from_id=4, to_id=3, meta_rel="PROTEIN_TO_GENE"),
        DiagramEdge(from_id=4, to_id=5, meta_rel="PROTEIN_IN_PATHWAY"),
    ]
    diagram = CypherDiagram(nodes=diagram_nodes, edges=diagram_edges)
    diagram_data = diagram.generate_diagram()
    return diagram_data
