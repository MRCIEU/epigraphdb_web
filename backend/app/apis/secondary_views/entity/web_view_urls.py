from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Set
from urllib.parse import urlencode

URL_MAPPER_METHODS = ["id", "name"]


@dataclass
class UrlTranslator:
    how: str
    prefix: Optional[str] = None
    # prefix_resolver: dealing with cases like mr exposures and outcomes
    prefix_resolver: Callable = None
    # source_prefix: Optional[str] = None
    # target_prefix: Optional[str] = None
    extra_params: Optional[Dict[str, Any]] = None

    def generate_url(
        self,
        root_url: str,
        entity_id: str,
        entity_name: str,
        entity_triples: Set[str],
    ) -> str:
        if self.prefix_resolver is None:
            prefix = self.prefix
        else:
            prefix = self.prefix_resolver(entity_triples)
        if self.how == "id":
            entity_expr = entity_id
        elif self.how == "name":
            entity_expr = entity_name
        default_param = {prefix: entity_expr}
        extra_params = {} if self.extra_params is None else self.extra_params
        params = {**default_param, **extra_params}
        query_expr = urlencode(params)
        url = f"{root_url}?{query_expr}"
        return url


def mr_prefix_resolver(entity_triples: Set[str]) -> str:
    triples = list(entity_triples)
    # when there are source and target cases, always prefer source
    if "(Gwas)-[MR_EVE_MR]->(Gwas)" in triples:
        return "exposure-query"
    else:
        return "outcome-query"


mr = {
    "Gwas": UrlTranslator(
        how="name",
        prefix_resolver=mr_prefix_resolver,
    )
}

obs_cor = {"Gwas": UrlTranslator(how="name", prefix="trait-query")}

genetic_cor = {"Gwas": UrlTranslator(how="name", prefix="trait-query")}

prs = {"Gwas": UrlTranslator(how="name", prefix="trait-query")}

pathway = {"Gwas": UrlTranslator(how="name", prefix="trait-query")}

# ontology_trait_disease = {
#     # "Gwas": UrlTranslator(how="name", prefix="trait-query"),
#     # "Efo": UrlTranslator(how="name", prefix="efo-term"),
#     # "Disease": UrlTranslator(how="name", prefix="disease-label"),
# }

literature_trait = {"Gwas": UrlTranslator(how="name", prefix="trait-query")}

web_view_urls = {
    "mr": mr,
    "genetic_cor": genetic_cor,
    "obs_cor": obs_cor,
    "prs": prs,
    "pathway": pathway,
    # "ontology_trait_disease": ontology_trait_disease,
    "literature_trait": literature_trait,
}
