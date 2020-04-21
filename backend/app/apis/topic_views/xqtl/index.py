from app.funcs.elasticsearch.autocomplete import index_ac_name_from_cypher
from app.funcs.elasticsearch.indexers import (
    name_indexer_edge_ngram_long,
    name_indexer_edge_ngram_short,
    name_indexer_standard,
)
from app.funcs.elasticsearch.query import query_ac_name, query_ac_name_prefix
from app.utils.database import es_client

ac_configs = {
    "exposure_gene": {
        "index_name": "ac_xqtl_exposure_gene",
        "indexer_fn": name_indexer_edge_ngram_short,
        "query_fn": query_ac_name,
        "query": """
            MATCH
                (gene:Gene)-[r:XQTL_SINGLE_SNP_MR_GENE_GWAS]->(gwas:Gwas)
            WHERE
                r.p < 0.1 AND gene.name is not null
            RETURN DISTINCT
                gene.name AS name
            ;
            """.replace(
            "\n", " "
        ),
    },
    "outcome_trait": {
        "index_name": "ac_xqtl_outcome_trait",
        "indexer_fn": name_indexer_edge_ngram_long,
        "query_fn": query_ac_name,
        "query": """
            MATCH
                (gene:Gene)-[r:XQTL_SINGLE_SNP_MR_GENE_GWAS]->(gwas:Gwas)
            WHERE
                r.p < 0.1 AND gene.name is not null
            RETURN DISTINCT
                gwas.trait AS name
            ;
            """.replace(
            "\n", " "
        ),
    },
    "variant": {
        "index_name": "ac_xqtl_variant",
        "indexer_fn": name_indexer_standard,
        "query_fn": query_ac_name_prefix,
        "query": """
            MATCH
                (variant:Variant)-[s:XQTL_SINGLE_SNP_MR_SNP_GENE]->(gene:Gene)
            WHERE
                variant.name is not null AND gene.name is not null
            RETURN DISTINCT
                variant.name AS name
            LIMIT
                2000;
            """.replace(
            "\n", " "
        ),
    },
}


def xqtl_index_name(overwrite: bool = False) -> bool:
    index_res = [
        index_ac_name_from_cypher(
            cypher_query=configs["query"],
            index_name=configs["index_name"],
            es_client=es_client,
            indexer_fn=configs["indexer_fn"],
            overwrite=overwrite,
        )
        for name, configs in ac_configs.items()
    ]
    res = sum(index_res) == len(index_res)
    return res
