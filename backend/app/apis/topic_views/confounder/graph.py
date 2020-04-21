from app.funcs.network_graph import NetworkEdgeSchema, NetworkNodeSchema
from app.utils.meta_graph import gwas_label_formatter, mr_eve_title_formatter

node_schemas = [
    NetworkNodeSchema(
        meta_node="GwasExposure",
        id_col="exposure.id",
        label_formatter=gwas_label_formatter(node_name="exposure"),
    ),
    NetworkNodeSchema(
        meta_node="GwasOutcome",
        id_col="outcome.id",
        label_formatter=gwas_label_formatter(node_name="outcome"),
    ),
    NetworkNodeSchema(
        meta_node="Gwas",
        id_col="cf.id",
        label_formatter=gwas_label_formatter(node_name="cf"),
    ),
]

edge_confounder_exposure = {
    "confounder": NetworkEdgeSchema(
        from_col="cf.id",
        to_col="exposure.id",
        from_meta_node="Gwas",
        dashes=True,
        hover_title_formatter=mr_eve_title_formatter(
            exposure_id="cf.id",
            outcome_id="exposure.id",
            estimate="r1.b",
            se="r1.se",
            p="r1.pval",
            selection="r1.selection",
            method="r1.method",
        ),
    ),
    "intermediate": NetworkEdgeSchema(
        from_col="exposure.id",
        to_col="cf.id",
        from_meta_node="GwasExposure",
        dashes=True,
        hover_title_formatter=mr_eve_title_formatter(
            exposure_id="exposure.id",
            outcome_id="cf.id",
            estimate="r1.b",
            se="r1.se",
            p="r1.pval",
            selection="r1.selection",
            method="r1.method",
        ),
    ),
    "reverse_intermediate": NetworkEdgeSchema(
        from_col="cf.id",
        to_col="exposure.id",
        from_meta_node="Gwas",
        dashes=True,
        hover_title_formatter=mr_eve_title_formatter(
            exposure_id="cf.id",
            outcome_id="exposure.id",
            estimate="r1.b",
            se="r1.se",
            p="r1.pval",
            selection="r1.selection",
            method="r1.method",
        ),
    ),
    "collider": NetworkEdgeSchema(
        from_col="exposure.id",
        to_col="cf.id",
        from_meta_node="Gwas",
        dashes=True,
        hover_title_formatter=mr_eve_title_formatter(
            exposure_id="exposure.id",
            outcome_id="cf.id",
            estimate="r1.b",
            se="r1.se",
            p="r1.pval",
            selection="r1.selection",
            method="r1.method",
        ),
    ),
}

edge_confounder_outcome = {
    "confounder": NetworkEdgeSchema(
        from_col="cf.id",
        to_col="outcome.id",
        from_meta_node="Gwas",
        dashes=True,
        hover_title_formatter=mr_eve_title_formatter(
            exposure_id="cf.id",
            outcome_id="outcome.id",
            estimate="r3.b",
            se="r3.se",
            p="r3.pval",
            selection="r3.selection",
            method="r3.method",
        ),
    ),
    "intermediate": NetworkEdgeSchema(
        from_col="cf.id",
        to_col="outcome.id",
        from_meta_node="Gwas",
        dashes=True,
        hover_title_formatter=mr_eve_title_formatter(
            exposure_id="cf.id",
            outcome_id="outcome.id",
            estimate="r3.b",
            se="r3.se",
            p="r3.pval",
            selection="r3.selection",
            method="r3.method",
        ),
    ),
    "reverse_intermediate": NetworkEdgeSchema(
        from_col="outcome.id",
        to_col="cf.id",
        from_meta_node="GwasOutcome",
        dashes=True,
        hover_title_formatter=mr_eve_title_formatter(
            exposure_id="outcome.id",
            outcome_id="cf.id",
            estimate="r3.b",
            se="r3.se",
            p="r3.pval",
            selection="r3.selection",
            method="r3.method",
        ),
    ),
    "collider": NetworkEdgeSchema(
        from_col="outcome.id",
        to_col="cf.id",
        from_meta_node="GwasOutcome",
        dashes=True,
        hover_title_formatter=mr_eve_title_formatter(
            exposure_id="outcome.id",
            outcome_id="cf.id",
            estimate="r3.b",
            se="r3.se",
            p="r3.pval",
            selection="r3.selection",
            method="r3.method",
        ),
    ),
}


def create_edge_schemas(type: str = "confounder"):
    edge_schemas = [
        NetworkEdgeSchema(
            from_col="exposure.id",
            to_col="outcome.id",
            from_meta_node="GwasExposure",
            hover_title_formatter=mr_eve_title_formatter(
                exposure_id="exposure.id",
                outcome_id="outcome.id",
                estimate="r2.b",
                se="r2.se",
                p="r2.pval",
                selection="r2.selection",
                method="r2.method",
            ),
        ),
        edge_confounder_exposure[type],
        edge_confounder_outcome[type],
    ]
    return edge_schemas
