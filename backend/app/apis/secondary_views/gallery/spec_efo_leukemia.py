# Deprecated, no evidence due to structural change in traits from ieu gwas db

from app.funcs.network_graph import NetworkEdgeSchema, NetworkNodeSchema

from .graph import GalleryGraph, GalleryQueryType, GallerySchema

efo_leukemia = GalleryGraph(
    name="efo_leukemia",
    title="EFO: Leukemia",
    description="""
        <p>
        Ontology (Experimental Factor Ontology) terms
        and GWAS that are related to the term Leukemia
        </p>
    """.replace(
        "\n", ""
    ),
    query="""
        MATCH
            (e:Efo {value: "leukemia"})<-[:EFO_CHILD_OF*1..5]-(eChild:Efo)
        WITH e, eChild
        OPTIONAL MATCH
            (g1:Gwas)--(eChild)
        OPTIONAL MATCH
            (g2:Gwas)--(e)
        RETURN
            e {.id, .type, .value},
            eChild {.id, .type, .value},
            g1 {.id, .trait},
            g2 {.id, .trait}
        LIMIT 5000;
    """,
    query_type=GalleryQueryType.cypher,
    schema=GallerySchema(
        nodes=[
            NetworkNodeSchema(
                meta_node="Gwas", id_col="g1.id", label_col="g1.trait"
            ),
            NetworkNodeSchema(
                meta_node="Gwas", id_col="g2.id", label_col="g2.trait"
            ),
            NetworkNodeSchema(
                meta_node="EfoPrimary", id_col="e.id", label_col="e.value"
            ),
            NetworkNodeSchema(
                meta_node="Efo", id_col="eChild.id", label_col="eChild.value"
            ),
        ],
        edges=[
            NetworkEdgeSchema(
                from_col="e.id", to_col="eChild.id", from_meta_node="Efo"
            ),
            NetworkEdgeSchema(
                from_col="eChild.id", to_col="g1.id", from_meta_node="Efo"
            ),
            NetworkEdgeSchema(
                from_col="e.id", to_col="g2.id", from_meta_node="Efo"
            ),
        ],
    ),
)
