from enum import Enum

from epigraphdb_common_utils.epigraphdb_data_dicts import (
    meta_nodes_dict_sanitised,
)


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


epigraphdb_meta_nodes = {
    key: {"id": value["id"], "name": value["name"]}
    for key, value in meta_nodes_dict_sanitised.items()
}


pqtl_meta_nodes_list = [
    "Instruments",
    "Sensitivity_Analysis",
    "Outcome",
    "Exposure",
]
