from enum import Enum
from typing import Dict

from typing_extensions import TypedDict

from epigraphdb_common_utils.epigraphdb_schema import meta_nodes_dict


class EpigraphdbMetaNode(str, Enum):
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
