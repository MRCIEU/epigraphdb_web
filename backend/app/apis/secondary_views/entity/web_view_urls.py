from dataclasses import dataclass
from typing import Any, Dict, Optional
from urllib.parse import urlencode

URL_MAPPER_METHODS = ["id", "name"]


@dataclass
class UrlTranslator:
    how: str
    prefix: Optional[str] = None
    source_prefix: Optional[str] = None
    target_prefix: Optional[str] = None
    extra_params: Optional[Dict[str, Any]] = None

    def generate_url(
        self,
        root_url: str,
        entity_id: str,
        entity_name: str,
        entity_node_type: str,
    ) -> str:
        if entity_node_type == "source" and self.source_prefix is not None:
            prefix = self.source_prefix
        elif entity_node_type == "target" and self.target_prefix is not None:
            prefix = self.target_prefix
        else:
            prefix = self.prefix
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


mr = {
    "Gwas": UrlTranslator(
        how="name",
        source_prefix="exposure-query",
        target_prefix="outcome-query",
    )
}

obs_cor = {"Gwas": UrlTranslator(how="name", prefix="trait-query")}

genetic_cor = {"Gwas": UrlTranslator(how="name", prefix="trait-query")}

prs = {"Gwas": UrlTranslator(how="name", prefix="trait-query")}

web_view_urls = {
    "mr": mr,
    "genetic_cor": genetic_cor,
    "obs_cor": obs_cor,
    "prs": prs,
}
