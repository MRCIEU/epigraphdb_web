from app.funcs.elasticsearch.indexers import (
    name_indexer_edge_ngram_long,
    name_indexer_edge_ngram_short,
    name_indexer_standard,
)

search_config = {
    "Gwas": {"indexer": name_indexer_edge_ngram_long},
    "Disease": {"indexer": name_indexer_edge_ngram_long},
    "Drug": {"indexer": name_indexer_edge_ngram_long},
    "Efo": {"indexer": name_indexer_edge_ngram_long},
    "Gene": {"indexer": name_indexer_edge_ngram_short},
    "Tissue": {"indexer": name_indexer_edge_ngram_long},
    "Pathway": {"indexer": name_indexer_edge_ngram_long},
    "Protein": {"indexer": name_indexer_edge_ngram_short},
    "LiteratureTerm": {
        "indexer": name_indexer_edge_ngram_long,
    },
    "Variant": {"indexer": name_indexer_standard},
}
