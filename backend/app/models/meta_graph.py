from enum import Enum
from typing import Dict

from typing_extensions import TypedDict

from epigraphdb_common_utils.epigraphdb_schema import meta_nodes_dict


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


class EpigraphdbMetaNodeForSearch(str, Enum):
    """Meta nodes to search. Exclude meta nodes that do not have meaningful
    labels, e.g. `(Literature)`, `(LiteratureTriple)`
    """

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


pqtl_meta_nodes_list = [
    "Instruments",
    "Sensitivity_Analysis",
    "Outcome",
    "Exposure",
]
