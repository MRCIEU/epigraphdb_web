from typing import Any, Dict, List, Optional, Union

from typing_extensions import TypedDict


class VisNodeColor(TypedDict, total=False):
    background: str
    highlight: Dict[str, str]
    hover: Dict[str, str]


class VisNodeFont(TypedDict, total=False):
    color: str


class VisNode(TypedDict, total=False):
    id: str
    label: str
    title: str
    url: str
    color: VisNodeColor
    shape: str
    font: VisNodeFont


class VisNode3d(TypedDict, total=False):
    id: str
    name: str
    color: str
    url: str


class VisEdgeArrows(TypedDict, total=False):
    to: bool


class VisEdgeScaling(TypedDict, total=False):
    min: Union[int, float]
    max: Union[int, float]


class VisEdgeColor(TypedDict, total=False):
    color: str
    hover: str


# NOTE: can't use class based defn given `from` is an attribute
VisEdge = TypedDict(
    "VisEdge",
    {
        "from": str,
        "to": str,
        "arrows": VisEdgeArrows,
        "scaling": VisEdgeScaling,
        "arrowStrikethrough": bool,
        "value": Union[int, float],
        "dashes": bool,
        "title": Optional[str],
        "color": VisEdgeColor,
    },
    total=False,
)


class VisEdge3d(TypedDict, total=False):
    source: str
    target: str
    color: str
    curvature: float
    rotation: float


class VisData(TypedDict):
    nodes: List[VisNode]
    edges: List[VisEdge]
    nodes_3d: List[VisNode3d]
    edges_3d: List[VisEdge3d]
    option: Dict[str, Any]
    num_paths_total: int
    num_paths_displayed: int
