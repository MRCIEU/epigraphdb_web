from typing import Any, Dict

from app.funcs.query_processors import (
    NetworkPlotSchemaInput,
    TopicQueryProcessor,
)

from .diagram import cypher_diagram
from .graph import create_edge_schemas, node_schemas

master_name = "confounder"
table_cols = [
    "cf.id",
    "cf.trait",
    "exposure.id",
    "exposure.trait",
    "outcome.id",
    "outcome.trait",
    "r1.b",
    "r1.method",
    "r1.moescore",
    "r1.pval",
    "r1.se",
    "r1.selection",
    "r2.b",
    "r2.method",
    "r2.moescore",
    "r2.pval",
    "r2.se",
    "r2.selection",
    "r3.b",
    "r3.method",
    "r3.moescore",
    "r3.pval",
    "r3.se",
    "r3.selection",
]


class ConfounderQueryProcessor(TopicQueryProcessor):
    def __init__(self, params: Dict[str, Any], type: str = "confounder"):
        super().__init__(
            master_name=master_name,
            params=params,
            table_cols=table_cols,
            network_plot_schema=NetworkPlotSchemaInput(
                node_schemas=node_schemas,
                edge_schemas=create_edge_schemas(type=type),
            ),
            cypher_diagram_fn=cypher_diagram,
        )
