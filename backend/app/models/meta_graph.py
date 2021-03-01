from enum import Enum


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
    # "Disease": {"id": "id", "name": "label"},
    # "Drug": {"id": "label", "name": "label"},
    # "Efo": {"id": "id", "name": "value"},
    # "Event": {"id": "reactome_id", "name": "name"},
    # "Gene": {"id": "ensembl_id", "name": "name"},
    # "Tissue": {"id": "tissue", "name": "tissue"},
    # "Gwas": {"id": "id", "name": "trait"},
    # "Literature": {"id": "id", "name": "id"},
    # "Pathway": {"id": "reactome_id", "name": "name"},
    # "Protein": {"id": "uniprot_id", "name": "uniprot_id"},
    # "LiteratureTerm": {"id": "id", "name": "name"},
    # "Variant": {"id": "name", "name": "name"},
    # TODO: switch to global scheme
    "Disease": {"id": "id", "name": "label"},
    "Drug": {"id": "id", "name": "value"},
    "Efo": {"id": "id", "name": "value"},
    "Gene": {"id": "ensembl_id", "name": "name"},
    "Tissue": {"id": "name", "name": "name"},
    "Gwas": {"id": "id", "name": "trait"},
    "Literature": {"id": "id", "name": "id"},
    "Pathway": {"id": "id", "name": "name"},
    "Protein": {"id": "uniprot_id", "name": "uniprot_id"},
    "LiteratureTerm": {"id": "id", "name": "name"},
    "Variant": {"id": "name", "name": "name"},
}

pqtl_meta_nodes_list = [
    "Instruments",
    "Sensitivity_Analysis",
    "Outcome",
    "Exposure",
]
