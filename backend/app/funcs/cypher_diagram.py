from dataclasses import dataclass
from typing import List, Optional

import pandas as pd

from app.models import cypher_diagram_models
from app.utils import hex_to_rgb
from app.utils.meta_graph import (
    color_palette,
    line_color_dict,
    meta_node_def,
    rel_def_url,
)
from app.utils.visjs_config import diagram_option, node_alpha

HIGHLIGHT_COLOR = color_palette["red"]["600"]


@dataclass
class DiagramNode:
    """
    - id: 1-indexed integer id
    - meta_node: Type of the node that should be referrable in the meta_graph
    - shape: visjs node shape
    """

    id: int
    meta_node: str
    label: Optional[str] = None
    sub_label: Optional[str] = None
    shape: str = "box"

    def __post_init__(self) -> None:
        if self.label is None:
            if self.sub_label is not None:
                self.label = f"{self.meta_node}\n{self.sub_label}"
            else:
                self.label = self.meta_node

    def generate_node(self):
        node = {
            "id": self.id,
            "label": self.label,
            "font": {"color": meta_node_def.loc[self.meta_node, "fg"]},
            "url": meta_node_def.loc[self.meta_node, "url"],
            "color": {
                "background": hex_to_rgb(
                    meta_node_def.loc[self.meta_node, "bg"], alpha=node_alpha
                ),
                "highlight": {
                    "background": meta_node_def.loc[self.meta_node, "bg"],
                    "border": HIGHLIGHT_COLOR,
                },
                "hover": {
                    "background": meta_node_def.loc[self.meta_node, "bg"],
                    "border": HIGHLIGHT_COLOR,
                },
            },
            "shape": "box",
        }
        return node


@dataclass
class DiagramEdge:
    """
    - from_id, to_id: 1-indexed integer id of the specific node
    - from_node: If specified, the edge will use the color of the node
    """

    from_id: int
    to_id: int
    meta_rel: Optional[str] = None
    label: Optional[str] = None
    sub_label: Optional[str] = None
    arrows: bool = True
    dashes: bool = False

    def __post_init__(self) -> None:
        self.url: Optional[str]
        if self.label is None:
            if self.meta_rel is not None and self.sub_label is not None:
                self.label = f"{self.meta_rel}\n{self.sub_label}"
            elif self.meta_rel is not None:
                self.label = self.meta_rel
        if self.meta_rel is not None:
            self.url = f"{rel_def_url}/{self.meta_rel}"
        else:
            self.url = None

    def generate_edge(self, node_df: pd.DataFrame):
        meta_node = node_df.at[self.from_id, "meta_node"]
        edge = {
            "from": self.from_id,
            "to": self.to_id,
            "arrows": {"to": self.arrows},
            "label": self.label,
            "url": self.url,
            "length": 100,
            "width": 2,
            "dashes": self.dashes,
            "color": {
                "color": meta_node_def.loc[meta_node, "bg"],
                "hover": line_color_dict["hover"],
            },
        }
        return edge


class CypherDiagram:
    def __init__(
        self,
        nodes: List[DiagramNode],
        edges: List[DiagramEdge],
        visjs_option=diagram_option,
    ):
        self.nodes = [node.generate_node() for node in nodes]
        nodes_df = pd.DataFrame(
            [{"id": node.id, "meta_node": node.meta_node} for node in nodes]
        ).set_index("id")
        self.edges = [edge.generate_edge(nodes_df) for edge in edges]
        self.option = visjs_option

    def generate_diagram(self) -> cypher_diagram_models.CypherDiagramData:
        self.diagram: cypher_diagram_models.CypherDiagramData = {
            "nodes": self.nodes,
            "edges": self.edges,
            "option": self.option,
        }
        return self.diagram
