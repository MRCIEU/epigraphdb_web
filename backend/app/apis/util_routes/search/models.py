from enum import Enum

from pydantic import BaseModel


class SearchEntityResponse(BaseModel):
    id: str
    name: str


class EpigraphdbMetaNode(str, Enum):
    Gwas = "Gwas"
    Disease = "Disease"
    Drug = "Drug"
    Efo = "Efo"
    Gene = "Gene"
    Literature = "Literature"
    LiteratureTerm = "LiteratureTerm"
    Pathway = "Pathway"
    Protein = "Protein"
    Tissue = "Tissue"
    Variant = "Variant"
