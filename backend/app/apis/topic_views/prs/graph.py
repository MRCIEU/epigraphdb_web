from app.funcs.network_graph import NetworkEdgeSchema, NetworkNodeSchema
from app.utils.meta_graph import gwas_label_formatter

node_schemas = [
    NetworkNodeSchema(
        meta_node="Gwas",
        id_col="trait.id",
        label_formatter=gwas_label_formatter(
            node_name=None, id_col="trait.id", trait_col="trait.trait"
        ),
    ),
    NetworkNodeSchema(
        meta_node="Gwas",
        id_col="assoc_trait.id",
        label_formatter=gwas_label_formatter(
            node_name=None,
            id_col="assoc_trait.id",
            trait_col="assoc_trait.trait",
        ),
    ),
]

edge_schemas = [
    NetworkEdgeSchema(
        from_col="trait.id",
        to_col="assoc_trait.id",
        from_meta_node="Gwas",
        meta_rel="PRS",
        arrows=False,
        hover_title_formatter=lambda row: None,
    )
]
