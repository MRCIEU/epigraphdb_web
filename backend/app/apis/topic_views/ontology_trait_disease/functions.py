from typing import Any, Dict, Optional

from app.funcs.cypher_diagram import CypherDiagram, DiagramEdge, DiagramNode
from app.funcs.query_processors import (
    NetworkPlotSchemaInput,
    TopicQueryProcessor,
)
from app.utils.data_table import NodeCol, RelCol
from app.utils.url_helpers import data_table_node_link, data_table_rel_link

from .graph import edge_schemas, node_schemas

master_name = "ontology_trait_disease"
api_endpoint = "ontology/gwas-efo-disease"
GWAS_DESC = "{Gwas} trait of interest.".format(
    Gwas=data_table_node_link("Gwas")
)
GE_DESC = """
Mapping from {Gwas} to {Efo} via semantic similarity {GWAS_NLP_EFO}.
""".format(
    Gwas=data_table_node_link("Gwas"),
    Efo=data_table_node_link("Efo"),
    GWAS_NLP_EFO=data_table_rel_link("GWAS_NLP_EFO"),
)
EFO_DESC = "Experimental Factor Ontology {Efo}".format(
    Efo=data_table_node_link("Efo")
)
DISEASE_DESC = "{Disease} term".format(Disease=data_table_node_link("Disease"))
table_col_configs = {
    "gwas.id": NodeCol("Gwas", "id", GWAS_DESC),
    "gwas.trait": NodeCol("Gwas", "trait", GWAS_DESC),
    "ge.score": RelCol("GWAS_NLP_EFO", "score", GE_DESC),
    "efo.type": NodeCol("Efo", "type", EFO_DESC),
    "efo.value": NodeCol("Efo", "value", EFO_DESC),
    "efo.id": NodeCol("Efo", "id", EFO_DESC),
    "disease.id": NodeCol("Disease", "id", DISEASE_DESC),
    "disease.label": NodeCol("Disease", "label", DISEASE_DESC),
}


class OntologyTraitDiseaseQueryProcessor(TopicQueryProcessor):
    def __init__(self, params: Dict[str, Any]):
        super().__init__(
            master_name=master_name,
            params=params,
            table_col_configs=table_col_configs,
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
