from typing import Any, Dict, List, Optional

import pandas as pd

from app.funcs.cypher_diagram import CypherDiagram, DiagramEdge, DiagramNode
from app.funcs.query_processors import (
    NetworkPlotSchemaInput,
    TopicQueryProcessor,
)
from app.utils.data_table import NodeCol, RelCol
from app.utils.url_helpers import data_table_node_link, data_table_rel_link

from .graph import edge_schemas, node_schemas

master_name = "literature_trait"
api_endpoint = "literature/gwas"
GWAS_DESC = "{Gwas} trait of interest.".format(
    Gwas=data_table_node_link("Gwas")
)
GS_DESC = "Association between {Gwas} and {SemmedTriple} via {GWAS_SEM}.".format(
    Gwas=data_table_node_link("Gwas"),
    SemmedTriple=data_table_node_link("SemmedTriple"),
    GWAS_SEM=data_table_rel_link("GWAS_SEM"),
)
TRIPLE_DESC = """
The SemMedDB knowledge triplet {SemmedTriple} that links the {Gwas} trait
with a SemMedDB term {SemmedTerm}.
""".format(
    SemmedTriple=data_table_node_link("SemmedTriple"),
    Gwas=data_table_node_link("Gwas"),
    SemmedTerm=data_table_node_link("SemmedTerm"),
)
LIT_DESC = """
{Literature} evidence regarding the {Gwas} trait as a PubMed article.
""".format(
    Literature=data_table_node_link("Literature"),
    Gwas=data_table_node_link("Gwas"),
)
table_col_configs = {
    "gwas.id": NodeCol("Gwas", "id", GWAS_DESC),
    "gwas.trait": NodeCol("Gwas", "trait", GWAS_DESC),
    "gs.pval": RelCol("GWAS_SEM", "pval", GS_DESC),
    "gs.localCount": RelCol("GWAS_SEM", "localCount", GS_DESC),
    "triple.id": NodeCol("SemmedTriple", "id", TRIPLE_DESC),
    "triple.subject_name": NodeCol(
        "SemmedTriple", "subject_name", TRIPLE_DESC
    ),
    "triple.object_name": NodeCol("SemmedTriple", "object_name", TRIPLE_DESC),
    "lit.pubmed_id": NodeCol("Literature", "pubmed_id", LIT_DESC),
}


def table_precaching_hook(df: pd.DataFrame) -> pd.DataFrame:
    res_df = df.sort_values(by=["gs.pval"], ascending=True).reset_index(
        drop=True
    )
    return res_df


class LiteratureTraitQueryProcessor(TopicQueryProcessor):
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
            table_precaching_hook=table_precaching_hook,
        )


def cypher_diagram(
    trait: str,
    semmed_predicates: Optional[List[str]],
    pval_threshold: float,
    limit: int,
):
    id = {"gwas": 1, "triple": 2, "lit": 3}
    diagram_nodes = [
        DiagramNode(id=id["gwas"], meta_node="Gwas", sub_label=trait),
        DiagramNode(id=id["lit"], meta_node="Literature"),
        DiagramNode(
            id=id["triple"],
            meta_node="SemmedTriple",
            sub_label=semmed_predicates[0]
            if semmed_predicates is not None
            else None,
        ),
    ]
    diagram_edges = [
        DiagramEdge(
            from_id=id["gwas"], to_id=id["triple"], meta_rel="GWAS_SEM"
        ),
        DiagramEdge(
            from_id=id["gwas"],
            to_id=id["lit"],
            meta_rel="GWAS_TO_LIT",
            arrows=False,
            dashes=True,
        ),
        DiagramEdge(
            from_id=id["triple"], to_id=id["lit"], meta_rel="SEM_TO_LIT"
        ),
    ]
    diagram = CypherDiagram(nodes=diagram_nodes, edges=diagram_edges)
    diagram_data = diagram.generate_diagram()
    return diagram_data
