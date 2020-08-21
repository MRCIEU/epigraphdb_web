from typing import Any, Dict

from app.funcs.cypher_diagram import CypherDiagram, DiagramEdge, DiagramNode
from app.funcs.query_processors import (
    NetworkPlotSchemaInput,
    TopicQueryProcessor,
)

from .graph import edge_schemas, node_schemas

master_name = "pathway"
table_cols = [
    "gwas.id",
    "gwas.trait",
    "gwas_to_variant.beta",
    "gwas_to_variant.se",
    "gwas_to_variant.pval",
    "gwas_to_variant.samplesize",
    "variant.name",
    "gene.name",
    "protein.uniprot_id",
    "pathway.reactome_id",
    "pathway.name",
]
cols_to_round = ["gwas_to_variant.beta", "gwas_to_variant.se"]


class PathwayQueryProcessor(TopicQueryProcessor):
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
