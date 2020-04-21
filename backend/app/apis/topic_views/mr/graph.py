from app.funcs.network_graph import NetworkEdgeSchema, NetworkNodeSchema
from app.utils.meta_graph import gwas_label_formatter, mr_eve_title_formatter

# NOTE: it is impossible to specify a study to be exposure or outcome
#       in the current api spec, as a study can be both exposure or outcome
#       each time.
node_schemas = [
    NetworkNodeSchema(
        meta_node="Gwas",
        id_col="exposure.id",
        label_formatter=gwas_label_formatter(
            node_name=None, id_col="exposure.id", trait_col="exposure.trait"
        ),
    ),
    NetworkNodeSchema(
        meta_node="Gwas",
        id_col="outcome.id",
        label_formatter=gwas_label_formatter(
            node_name=None, id_col="outcome.id", trait_col="outcome.trait"
        ),
    ),
]

edge_schemas = [
    NetworkEdgeSchema(
        from_col="exposure.id",
        to_col="outcome.id",
        from_meta_node="Gwas",
        hover_title_formatter=mr_eve_title_formatter(
            exposure_id="exposure.id", outcome_id="outcome.id"
        ),
    )
]
