from enum import Enum
from typing import Any, List, Optional

from pydantic import BaseModel


class SearchEntityResponse(BaseModel):
    id: str
    name: str
    meta_node: str


class SearchFullResponse(BaseModel):
    results: List[Optional[SearchEntityResponse]]
    summary: Any


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
