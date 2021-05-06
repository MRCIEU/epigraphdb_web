from app.funcs.elasticsearch.indexers import (
    name_indexer_edge_ngram_long,
    name_indexer_edge_ngram_short,
    name_indexer_standard,
)

# TODO: fetch num ents upstream
search_config = {
    "Gwas": {"length": 35_000, "indexer": name_indexer_edge_ngram_long},
    "Disease": {"length": 25_000, "indexer": name_indexer_edge_ngram_long},
    "Drug": {"length": 2_500, "indexer": name_indexer_edge_ngram_long},
    "Efo": {"length": 26_000, "indexer": name_indexer_edge_ngram_long},
    "Gene": {"length": 60_000, "indexer": name_indexer_edge_ngram_short},
    "Tissue": {"length": 12_000, "indexer": name_indexer_edge_ngram_long},
    "Pathway": {"length": 2_200, "indexer": name_indexer_edge_ngram_long},
    "Protein": {"length": 22_000, "indexer": name_indexer_edge_ngram_short},
    "LiteratureTerm": {
        "length": 10_6000,
        "indexer": name_indexer_edge_ngram_long,
    },
    "Variant": {"length": 90_000, "indexer": name_indexer_standard},
}
