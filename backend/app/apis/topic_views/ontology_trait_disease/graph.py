from app.funcs.network_graph import NetworkEdgeSchema, NetworkNodeSchema
from app.utils.meta_graph import gwas_label_formatter

node_schemas = [
    NetworkNodeSchema(
        id_col="gwas.id",
        label_formatter=gwas_label_formatter(node_name="gwas"),
        meta_node="Gwas",
    ),
    NetworkNodeSchema(id_col="efo.id", label_col="efo.value", meta_node="Efo"),
    NetworkNodeSchema(
        id_col="disease.id", label_col="disease.label", meta_node="Disease"
    ),
]

edge_schemas = [
    NetworkEdgeSchema(
        from_col="gwas.id",
        to_col="efo.id",
        from_meta_node="Gwas",
        arrows=False,
    ),
    NetworkEdgeSchema(
        from_col="efo.id",
        to_col="disease.id",
        from_meta_node="Disease",
        arrows=False,
    ),
]
