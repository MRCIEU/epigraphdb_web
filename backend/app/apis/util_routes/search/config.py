from app.funcs.elasticsearch.indexers import (
    name_indexer_edge_ngram_long,
    name_indexer_edge_ngram_short,
    name_indexer_standard,
)

search_config = {
    "Gwas": {"length": 35000, "indexer": name_indexer_edge_ngram_long},
    "Disease": {"length": 25000, "indexer": name_indexer_edge_ngram_long},
    "Drug": {"length": 2500, "indexer": name_indexer_edge_ngram_long},
    "Efo": {"length": 26000, "indexer": name_indexer_edge_ngram_long},
    "Gene": {"length": 60000, "indexer": name_indexer_edge_ngram_short},
    "Tissue": {"length": 12000, "indexer": name_indexer_edge_ngram_long},
    "Pathway": {"length": 2200, "indexer": name_indexer_edge_ngram_long},
    "Protein": {"length": 22000, "indexer": name_indexer_edge_ngram_short},
    "LiteratureTerm": {
        "length": 106000,
        "indexer": name_indexer_edge_ngram_long,
    },
    "Variant": {"length": 90000, "indexer": name_indexer_standard},
}
