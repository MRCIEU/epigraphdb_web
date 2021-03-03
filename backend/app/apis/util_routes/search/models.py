from enum import Enum

from pydantic import BaseModel


class SearchEntityResponse(BaseModel):
    id: str
    name: str


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
