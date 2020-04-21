from app.funcs.network_graph import NetworkEdgeSchema, NetworkNodeSchema
from app.utils.meta_graph import gwas_label_formatter, mr_eve_title_formatter

node_schemas = [
    NetworkNodeSchema(
        meta_node="GwasExposure",
        id_col="trait.id",
        label_formatter=gwas_label_formatter(node_name="trait"),
    ),
    NetworkNodeSchema(
        meta_node="Gwas",
        id_col="assoc_trait.id",
        label_formatter=gwas_label_formatter(node_name="assoc_trait"),
    ),
    NetworkNodeSchema(meta_node="Variant", id_col="variant.name"),
    NetworkNodeSchema(
        meta_node="Gene", id_col="gene.name", match_node_by="name"
    ),
    NetworkNodeSchema(meta_node="Drug", id_col="drug.label"),
]

edge_schemas = [
    NetworkEdgeSchema(
        from_col="assoc_trait.id",
        to_col="trait.id",
        from_meta_node="Gwas",
        hover_title_formatter=mr_eve_title_formatter(
            exposure_id="assoc_trait.id",
            outcome_id="trait.id",
            estimate="mr.b",
            se="mr.se",
            p="mr.pval",
            selection="mr.selection",
            method="mr.method",
        ),
    ),
    NetworkEdgeSchema(
        from_col="variant.name", to_col="assoc_trait.id", from_meta_node="Gwas"
    ),
    NetworkEdgeSchema(
        from_col="variant.name", to_col="gene.name", from_meta_node="Variant"
    ),
    NetworkEdgeSchema(
        from_col="drug.label", to_col="gene.name", from_meta_node="Drug"
    ),
]
