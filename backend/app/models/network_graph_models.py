from typing import Any, Dict, List, Union

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


# NOTE:
# can't fully use class based defn given `from` is an attribute
# yet pydantic (1.8) compatibility with object based
# typeddict defn is not good (totality).
VisEdgeBase = TypedDict(
    "VisEdgeBase",
    {
        "from": str,
        "to": str,
        "arrows": VisEdgeArrows,
        "dashes": bool,
        "color": VisEdgeColor,
    },
)


class VisEdge(VisEdgeBase, total=False):
    scaling: VisEdgeScaling
    arrowStrikethrough: bool
    value: Union[int, float]
    title: str
    url: str
    label: str
    length: int
    width: int


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
