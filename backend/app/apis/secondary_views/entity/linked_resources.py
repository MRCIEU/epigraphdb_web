from typing import Optional

from .models import LinkedResource

linked_resources = {
    "Gwas": {
        "uri": "https://gwas.mrcieu.ac.uk/gwas/{id}/",
        "url": "https://gwas.mrcieu.ac.uk",
        "resource_name": "OpenGwas",
        "logo": "open-gwas-logo.png",
    },
    "Literature": {
        "uri": "https://www.ncbi.nlm.nih.gov/pubmed/{id}",
        "url": "https://www.ncbi.nlm.nih.gov/pubmed",
        "resource_name": "PubMed",
        "logo": "PubMed.png",
    },
    "Efo": {
        "uri": "{id}",
        "url": "https://www.ebi.ac.uk/efo/",
        "resource_name": "Experimental Factor Ontology",
        "logo": "efo-logo.gif",
    },
}


def map_linked_external_resource(
    meta_node: str, id: Optional[str]
) -> Optional[LinkedResource]:
    if meta_node not in linked_resources.keys():
        return None
    else:
        resource = linked_resources[meta_node]
        if id is not None:
            url = resource["uri"].format(id=id)
        else:
            url = resource["url"]
        res: LinkedResource = {
            "name": resource["resource_name"],
            "url": url,
            "logo": resource["logo"],
        }
        return res
