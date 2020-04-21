from typing import Any, Dict, Optional

from app.funcs.cypher_diagram import CypherDiagram, DiagramEdge, DiagramNode
from app.funcs.query_processors import (
    NetworkPlotSchemaInput,
    TopicQueryProcessor,
)

from .graph import edge_schemas, node_schemas

master_name = "ontology_trait_disease"
api_endpoint = "ontology/gwas-efo-disease"
table_cols = [
    "gwas.id",
    "gwas.trait",
    "ge.score",
    "efo.type",
    "efo.value",
    "efo.id",
    "disease.id",
    "disease.label",
]


class OntologyTraitDiseaseQueryProcessor(TopicQueryProcessor):
    def __init__(self, params: Dict[str, Any]):
        super().__init__(
            master_name=master_name,
            params=params,
            table_cols=table_cols,
            network_plot_schema=NetworkPlotSchemaInput(
                node_schemas=node_schemas, edge_schemas=edge_schemas
            ),
            api_endpoint=api_endpoint,
            cypher_diagram_fn=cypher_diagram,
        )


def cypher_diagram(
    trait: Optional[str],
    efo_term: Optional[str],
    disease_label: Optional[str],
    score_threshold: float,
):
    id = {"gwas": 1, "efo": 2, "disease": 3}
    diagram_nodes = [
        DiagramNode(id=id["gwas"], meta_node="Gwas", sub_label=trait),
        DiagramNode(id=id["efo"], meta_node="Efo", sub_label=efo_term),
        DiagramNode(
            id=id["disease"], meta_node="Disease", sub_label=disease_label
        ),
    ]
    edge_label = (
        f"score > {score_threshold}" if score_threshold is not None else ""
    )
    diagram_edges = [
        DiagramEdge(
            from_id=id["gwas"],
            to_id=id["efo"],
            meta_rel="GWAS_NLP_EFO",
            arrows=False,
            sub_label=edge_label,
        ),
        DiagramEdge(
            from_id=id["efo"],
            to_id=id["disease"],
            meta_rel="MONDO_MAP_EFO",
            arrows=False,
        ),
    ]
    diagram = CypherDiagram(nodes=diagram_nodes, edges=diagram_edges)
    diagram_data = diagram.generate_diagram()
    return diagram_data
