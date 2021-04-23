from typing import Optional

from .models import LinkedResource

linked_resources = {
    "Gwas": {
        "url": "https://gwas.mrcieu.ac.uk/gwas/{id}/",
        "resource_name": "OpenGwas",
        "logo": "open-gwas-logo.png",
    },
    "Literature": {
        "url": "https://www.ncbi.nlm.nih.gov/pubmed/{id}",
        "resource_name": "PubMed",
        "logo": "PubMed.png",
    },
    "Efo": {
        "url": "{id}",
        "resource_name": "Experimental Factor Ontology",
        "logo": "efo-logo.gif",
    },
}


def map_linked_external_resource(
    meta_node: str, id: str
) -> Optional[LinkedResource]:
    if meta_node not in linked_resources.keys():
        return None
    else:
        resource = linked_resources[meta_node]
        res: LinkedResource = {
            "name": resource["resource_name"],
            "url": resource["url"].format(id=id),
            "logo": resource["logo"],
        }
        return res
