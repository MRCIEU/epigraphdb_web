from app.funcs.network_graph import NetworkEdgeSchema, NetworkNodeSchema

single_snp_mr_title_formatter = lambda row: """
    <b>exposure_ensembl_id</b>: {exposure_ensembl_id},
    <b>outcome_id</b>: {outcome_id}</br>
    <b>rsid</b>: {rsid}</br>
    <b>b</b>: {b:.2E}, <b>se</b>: {se:.2E}, <b>p</b>: {p:.2E}
    """.format(
    exposure_ensembl_id=row["gene.ensembl_id"],
    outcome_id=row["gwas.id"],
    rsid=row["r.rsid"],
    b=row["r.beta"],
    se=row["r.se"],
    p=row["r.p"],
)


multi_snp_mr_title_formatter = lambda row: """
    <b>exposure_ensembl_id</b>: {exposure_ensembl_id},
    <b>outcome_id</b>: {outcome_id}</br>
    <b>b</b>: {b:.2E}, <b>se</b>: {se:.2E}, <b>p</b>: {p:.2E}
    """.format(
    exposure_ensembl_id=row["gene.ensembl_id"],
    outcome_id=row["gwas.id"],
    b=row["r.beta"],
    se=row["r.se"],
    p=row["r.p"],
)

node_schemas_single_snp = [
    NetworkNodeSchema(
        meta_node="Gene", id_col="gene.ensembl_id", label_col="gene.name"
    ),
    NetworkNodeSchema(
        meta_node="Gwas",
        id_col="gwas.id",
        label_formatter=lambda row: "{id}: {name}".format(
            id=row["gwas.id"], name=row["gwas.trait"]
        ),
    ),
    NetworkNodeSchema(meta_node="Variant", id_col="r.rsid"),
]

node_schemas_multi_snp = [
    NetworkNodeSchema(
        meta_node="Gene", id_col="gene.ensembl_id", label_col="gene.name"
    ),
    NetworkNodeSchema(
        meta_node="Gwas",
        id_col="gwas.id",
        label_formatter=lambda row: "{id}: {name}".format(
            id=row["gwas.id"], name=row["gwas.trait"]
        ),
    ),
]

edge_schemas_single_snp = [
    NetworkEdgeSchema(
        from_col="gene.ensembl_id",
        to_col="gwas.id",
        from_meta_node="Gene",
        hover_title_formatter=single_snp_mr_title_formatter,
    ),
    NetworkEdgeSchema(
        from_col="r.rsid", to_col="gene.ensembl_id", from_meta_node="Variant"
    ),
]

edge_schemas_multi_snp = [
    NetworkEdgeSchema(
        from_col="gene.ensembl_id",
        to_col="gwas.id",
        from_meta_node="Gene",
        hover_title_formatter=multi_snp_mr_title_formatter,
    )
]
