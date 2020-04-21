from app.funcs.network_graph import NetworkEdgeSchema, NetworkNodeSchema
from app.utils.meta_graph import gwas_label_formatter

node_schemas = [
    NetworkNodeSchema(
        meta_node="Gwas",
        id_col="gwas.id",
        label_formatter=gwas_label_formatter(),
    ),
    NetworkNodeSchema(
        meta_node="Variant", id_col="variant.name", label_col="variant.name"
    ),
    NetworkNodeSchema(
        meta_node="Gene",
        id_col="gene.name",
        label_col="gene.name",
        match_node_by="name",
    ),
    NetworkNodeSchema(
        meta_node="Protein",
        id_col="protein.uniprot_id",
        label_col="protein.uniprot_id",
    ),
    NetworkNodeSchema(
        meta_node="Pathway",
        id_col="pathway.name",
        label_col="pathway.name",
        match_node_by="name",
    ),
]
edge_schemas = [
    NetworkEdgeSchema(
        to_col="variant.name",
        from_col="gwas.id",
        from_meta_node="Gwas",
        hover_title_formatter=lambda row: """
                    <b>gwas.id</b>: {gwas_id},
                    <b>variant.name</b>: {variant_name}</br>
                    <b>beta</b>: {beta:.2E},
                    <b>se</b>: {se:.2E},
                    <b>pval</b>: {pval:.2E}
                    """.format(
            gwas_id=row["gwas.id"],
            variant_name=row["variant.name"],
            beta=row["gwas_to_variant.beta"],
            se=row["gwas_to_variant.se"],
            pval=row["gwas_to_variant.pval"],
        ),
    ),
    NetworkEdgeSchema(
        from_col="variant.name", to_col="gene.name", from_meta_node="Variant"
    ),
    NetworkEdgeSchema(
        from_col="gene.name",
        to_col="protein.uniprot_id",
        from_meta_node="Gene",
    ),
    NetworkEdgeSchema(
        from_col="protein.uniprot_id",
        to_col="pathway.name",
        from_meta_node="Protein",
    ),
]
