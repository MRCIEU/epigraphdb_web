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
    Event = "Event"
    Gene = "Gene"
    Gtex = "Gtex"
    # # Literature = "Literature"
    Pathway = "Pathway"
    Protein = "Protein"
    SemmedTerm = "SemmedTerm"
    Variant = "Variant"
