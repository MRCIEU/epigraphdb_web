from typing import Any, Dict, List

from typing_extensions import TypedDict

from . import network_graph_models


class CypherDiagramData(TypedDict):
    nodes: List[network_graph_models.VisNode]
    edges: List[network_graph_models.VisEdge]
    option: Dict[str, Any]
