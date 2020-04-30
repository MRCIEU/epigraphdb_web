from app.funcs.network_graph import NetworkEdgeSchema, NetworkNodeSchema
from app.utils.meta_graph import gwas_label_formatter

node_schemas = [
    NetworkNodeSchema(
        id_col="gwas.id",
        label_formatter=gwas_label_formatter(node_name="gwas"),
        meta_node="Gwas",
    ),
    NetworkNodeSchema(id_col="triple.id", meta_node="SemmedTriple"),
    NetworkNodeSchema(id_col="lit.pubmed_id", meta_node="Literature"),
]

edge_schemas = [
    NetworkEdgeSchema(
        from_col="gwas.id", to_col="triple.id", from_meta_node="Gwas"
    ),
    NetworkEdgeSchema(
        from_col="gwas.id",
        to_col="lit.pubmed_id",
        from_meta_node="Gwas",
        arrows=False,
        dashes=True,
    ),
    NetworkEdgeSchema(
        from_col="triple.id",
        to_col="lit.pubmed_id",
        from_meta_node="SemmedTriple",
    ),
]
