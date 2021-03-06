from enum import Enum
from typing import Dict

from typing_extensions import TypedDict

from epigraphdb_common_utils.epigraphdb_schema import (
    meta_nodes_dict,
    meta_rels_dict,
)


class EpigraphdbMetaNodeFull(str, Enum):
    Disease = "Disease"
    Drug = "Drug"
    Efo = "Efo"
    Gene = "Gene"
    Tissue = "Tissue"
    Gwas = "Gwas"
    Literature = "Literature"
    Pathway = "Pathway"
    Protein = "Protein"
    LiteratureTerm = "LiteratureTerm"
    LiteratureTriple = "LiteratureTriple"
    Variant = "Variant"


class EpigraphdbMetaNodeNonCodeName(str, Enum):
    """Meta nodes with meaningful names, but not necessarily
    used in indexing.
    """

    Gwas = "Gwas"
    Disease = "Disease"
    Drug = "Drug"
    Efo = "Efo"
    LiteratureTerm = "LiteratureTerm"
    LiteratureTriple = "LiteratureTriple"
    Pathway = "Pathway"
    Tissue = "Tissue"


class EpigraphdbMetaNodeForSearch(str, Enum):
    """Meta nodes with meaningful names indexable and searchable."""

    Gwas = "Gwas"
    Disease = "Disease"
    Drug = "Drug"
    Efo = "Efo"
    Gene = "Gene"
    LiteratureTerm = "LiteratureTerm"
    Pathway = "Pathway"
    Protein = "Protein"
    Tissue = "Tissue"
    Variant = "Variant"


class MetaNodeInfo(TypedDict):
    id: str
    name: str


epigraphdb_meta_nodes: Dict[str, MetaNodeInfo] = {
    key: {"id": value.id, "name": value.name}
    for key, value in meta_nodes_dict.items()
}

EpigraphdbMetaRelFull = Enum(  # type: ignore
    "EpigraphdbMetaRelFull", {_: _ for _ in meta_rels_dict.keys()}
)

pqtl_meta_nodes_list = [
    "Instruments",
    "Sensitivity_Analysis",
    "Outcome",
    "Exposure",
]
