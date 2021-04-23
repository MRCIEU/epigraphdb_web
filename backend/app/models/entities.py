from typing_extensions import TypedDict


class AnnotatedMetaEntity(TypedDict):
    name: str
    doc: str
    url: str


class AnnotatedNodeId(TypedDict):
    id: str
    url: str


class AnnotatedProperty(TypedDict):
    prop_name: str
    doc: str
