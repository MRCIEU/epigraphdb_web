from typing import Any, Dict

from app.funcs.query_processors import (
    NetworkPlotSchemaInput,
    TopicQueryProcessor,
)
from app.utils.data_table import NodeCol, RelCol
from app.utils.url_helpers import data_table_node_link, data_table_rel_link

from .diagram import cypher_diagram
from .graph import create_edge_schemas, node_schemas

master_name = "confounder"
EXPOSURE_DESC = "Exposure {gwas}.".format(gwas=data_table_node_link("Gwas"))
OUTCOME_DESC = "Outcome {gwas}".format(gwas=data_table_node_link("Gwas"))
CF_DESC = """
Confounder* {gwas}.

*subject to the option `confounder_type`, `cf`
can be a confounder, intermediate, reverse intermediate, or collider
(see documentation for further details).
""".format(
    gwas=data_table_node_link("Gwas")
)
R1_DESC = """
{MR_EVE_MR} between exposure and `cf`.

Direction of the MR evidence is determined by `confounder_type`
(see documentation for further details).
""".format(
    MR_EVE_MR=data_table_rel_link("MR_EVE_MR")
)
R2_DESC = """
{MR_EVE_MR} from exposure to outcome.
""".format(
    MR_EVE_MR=data_table_rel_link("MR_EVE_MR")
)
R3_DESC = """
{MR_EVE_MR} between outcome and `cf`.

Direction of the MR evidence is determined by `confounder_type`
(see documentation for further details).
""".format(
    MR_EVE_MR=data_table_rel_link("MR_EVE_MR")
)
table_col_configs = {
    "cf.id": NodeCol("Gwas", "id", CF_DESC),
    "cf.trait": NodeCol("Gwas", "trait", CF_DESC),
    "exposure.id": NodeCol("Gwas", "id", EXPOSURE_DESC),
    "exposure.trait": NodeCol("Gwas", "trait", EXPOSURE_DESC),
    "outcome.id": NodeCol("Gwas", "id", OUTCOME_DESC),
    "outcome.trait": NodeCol("Gwas", "trait", OUTCOME_DESC),
    "r1.b": RelCol("MR_EVE_MR", "b", R1_DESC, rounding=True),
    "r1.method": RelCol("MR_EVE_MR", "method", R1_DESC),
    "r1.moescore": RelCol("MR_EVE_MR", "moescore", R1_DESC),
    "r1.pval": RelCol("MR_EVE_MR", "pval", R1_DESC),
    "r1.se": RelCol("MR_EVE_MR", "se", R1_DESC, rounding=True),
    "r1.selection": RelCol("MR_EVE_MR", "selection", R1_DESC),
    "r2.b": RelCol("MR_EVE_MR", "b", R2_DESC, rounding=True),
    "r2.method": RelCol("MR_EVE_MR", "method", R2_DESC),
    "r2.moescore": RelCol("MR_EVE_MR", "moescore", R2_DESC),
    "r2.pval": RelCol("MR_EVE_MR", "se", R2_DESC),
    "r2.se": RelCol("MR_EVE_MR", "se", R2_DESC, rounding=True),
    "r2.selection": RelCol("MR_EVE_MR", "selection", R2_DESC),
    "r3.b": RelCol("MR_EVE_MR", "b", R3_DESC, rounding=True),
    "r3.method": RelCol("MR_EVE_MR", "method", R3_DESC),
    "r3.moescore": RelCol("MR_EVE_MR", "moescore", R3_DESC),
    "r3.pval": RelCol("MR_EVE_MR", "pval", R3_DESC),
    "r3.se": RelCol("MR_EVE_MR", "se", R3_DESC, rounding=True),
    "r3.selection": RelCol("MR_EVE_MR", "selection", R3_DESC),
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
