from app.funcs.network_graph import NetworkEdgeSchema, NetworkNodeSchema

from .graph import GalleryGraph, GalleryQueryType, GallerySchema

confounder_bmi_chd = GalleryGraph(
    name="confounder_bmi_chd",
    title="Confounder: between Body mass index and Coronary heart disease",
    description="""
        <p>
        Traits that are identified to be causally related to the exposure-outcome pair
        as confounders from the evidence of MR-EvE.
        In this case the exposure trait is Body mass index (id: ieu-a-95)
        and outcome trait is Coronary heart disease (id: ieu-a-7).
        </p>

        <p>
        Visit <a href='https://epigraphdb.org/confounder/'>
        https://epigraphdb.org/confounder/</a>
        for more details.
        </p>
    """.replace(
        "\n", ""
    ),
    query="""
        MATCH
            (cf:Gwas)-[r1:MR]->
            (exposure:Gwas {id: "ieu-a-95"}) -[r2:MR]->
            (outcome:Gwas {id: "ieu-a-7"}) <-[r3:MR]-(cf:Gwas)
        WHERE
            r1.pval < 1e-05 AND r2.pval < 1e-05 AND r3.pval < 1e-05
            AND cf.id <> exposure.id AND cf.id <> outcome.id
            AND exposure.id <> outcome.id AND cf.trait <> exposure.trait
            AND cf.trait <> outcome.trait AND exposure.trait <> outcome.trait
        RETURN
            exposure {.id, .trait},
            outcome {.id, .trait},
            cf {.id, .trait},
            r1 {.b, .se, .pval, .selection, .method, .moescore},
            r2 {.b, .se, .pval, .selection, .method, .moescore},
            r3 {.b, .se, .pval, .selection, .method, .moescore}
        ORDER BY r1.pval;
    """,
    query_type=GalleryQueryType.cypher,
    schema=GallerySchema(
        nodes=[
            NetworkNodeSchema(
                meta_node="Gwas", id_col="cf.id", label_col="cf.trait"
            ),
            NetworkNodeSchema(
                meta_node="GwasExposure",
                id_col="exposure.id",
                label_col="exposure.trait",
            ),
            NetworkNodeSchema(
                meta_node="GwasOutcome",
                id_col="outcome.id",
                label_col="outcome.trait",
            ),
        ],
        edges=[
            NetworkEdgeSchema(
                from_col="cf.id", to_col="exposure.id", from_meta_node="Gwas"
            ),
            NetworkEdgeSchema(
                from_col="exposure.id",
                to_col="outcome.id",
                from_meta_node="GwasExposure",
            ),
            NetworkEdgeSchema(
                from_col="cf.id",
                to_col="outcome.id",
                from_meta_node="GwasOutcome",
            ),
        ],
    ),
)
