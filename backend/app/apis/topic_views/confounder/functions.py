from typing import Any, Dict

from app.funcs.query_processors import (
    NetworkPlotSchemaInput,
    TopicQueryProcessor,
)
from app.utils.data_table import NodeCol, RelCol

from .diagram import cypher_diagram
from .graph import create_edge_schemas, node_schemas

master_name = "confounder"
EXPOSURE_DESC = ""
OUTCOME_DESC = ""
CF_DESC = ""
R1_DESC = ""
R2_DESC = ""
R3_DESC = ""
table_col_configs = {
    "cf.id": NodeCol("Gwas", "id", CF_DESC),
    "cf.trait": NodeCol("Gwas", "trait", CF_DESC),
    "exposure.id": NodeCol("Gwas", "id", EXPOSURE_DESC),
    "exposure.trait": NodeCol("Gwas", "trait", EXPOSURE_DESC),
    "outcome.id": NodeCol("Gwas", "id", OUTCOME_DESC),
    "outcome.trait": NodeCol("Gwas", "trait", OUTCOME_DESC),
    "r1.b": RelCol("MR", "b", R1_DESC, rounding=True),
    "r1.method": RelCol("MR", "method", R1_DESC),
    "r1.moescore": RelCol("MR", "moescore", R1_DESC),
    "r1.pval": RelCol("MR", "pval", R1_DESC),
    "r1.se": RelCol("MR", "se", R1_DESC, rounding=True),
    "r1.selection": RelCol("MR", "selection", R1_DESC),
    "r2.b": RelCol("MR", "b", R2_DESC, rounding=True),
    "r2.method": RelCol("MR", "method", R2_DESC),
    "r2.moescore": RelCol("MR", "moescore", R2_DESC),
    "r2.pval": RelCol("MR", "se", R2_DESC),
    "r2.se": RelCol("MR", "se", R2_DESC, rounding=True),
    "r2.selection": RelCol("MR", "selection", R2_DESC),
    "r3.b": RelCol("MR", "b", R3_DESC, rounding=True),
    "r3.method": RelCol("MR", "method", R3_DESC),
    "r3.moescore": RelCol("MR", "moescore", R3_DESC),
    "r3.pval": RelCol("MR", "pval", R3_DESC),
    "r3.se": RelCol("MR", "se", R3_DESC, rounding=True),
    "r3.selection": RelCol("MR", "selection", R3_DESC),
}


class ConfounderQueryProcessor(TopicQueryProcessor):
    def __init__(self, params: Dict[str, Any], type: str = "confounder"):
        super().__init__(
            master_name=master_name,
            params=params,
            table_col_configs=table_col_configs,
            network_plot_schema=NetworkPlotSchemaInput(
                node_schemas=node_schemas,
                edge_schemas=create_edge_schemas(type=type),
            ),
            cypher_diagram_fn=cypher_diagram,
        )
