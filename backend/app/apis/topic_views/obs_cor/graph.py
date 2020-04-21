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
        arrows=False,
        meta_rel="OBS_COR",
        hover_title_formatter=lambda row: """
    <b>trait.id</b>: {trait_id} <b>assoc_trait.id</b>: {assoc_trait_id} </br>
    <b>cor</b>: {cor:.2f}
    """.format(
            trait_id=row["trait.id"],
            assoc_trait_id=row["assoc_trait.id"],
            cor=row["obs_cor.cor"],
        ),
    )
]
