from app.funcs.network_graph import NetworkEdgeSchema, NetworkNodeSchema

from .graph import GalleryGraph, GalleryQueryType, GallerySchema

gwas_bmi_gwas = GalleryGraph(
    name="gwas_bmi_gwas",
    title="GWAS: Associations",
    description="""
    """.replace(
        "\n", ""
    ),
    query="""
        MATCH
            (gwas:Gwas {id: "ieu-a-2"})-[mr:MR_EVE_MR]->(assoc_gwas:Gwas)
        WHERE
            mr.pval < 1e-05 AND
            assoc_gwas.trait <> gwas.trait
        OPTIONAL MATCH
            (gwas)-[prs1:PRS]-(assoc_gwas2:Gwas)-[prs2:PRS]-(assoc_gwas)
        WHERE
            prs1.p < 1e-05 AND prs2.p < 1e-05 AND
            assoc_gwas.trait <> gwas.trait AND gwas.trait <> assoc_gwas2.trait AND assoc_gwas2.trait <> assoc_gwas.trait
        OPTIONAL MATCH
            (gwas)-[obs_cor1:OBS_COR]-(assoc_gwas2:Gwas)-[obs_cor2:OBS_COR]-(assoc_gwas)
        WHERE
            assoc_gwas.trait <> gwas.trait AND gwas.trait <> assoc_gwas2.trait AND assoc_gwas2.trait <> assoc_gwas.trait
        OPTIONAL MATCH
            (gwas)-[gwas_nlp1:GWAS_NLP]-(assoc_gwas2:Gwas)-[gwas_nlp2:GWAS_NLP]-(assoc_gwas)
        WHERE
            assoc_gwas.trait <> gwas.trait AND gwas.trait <> assoc_gwas2.trait AND assoc_gwas2.trait <> assoc_gwas.trait
        RETURN
            gwas, assoc_gwas, assoc_gwas2,
            mr,
            obs_cor1, obs_cor2,
            prs1, prs2,
            gwas_nlp1, gwas_nlp2
        ORDER BY
            mr.pval
        LIMIT 100
    """,
    query_type=GalleryQueryType.cypher,
    schema=GallerySchema(
        nodes=[
            NetworkNodeSchema(
                meta_node="GwasPrimary",
                id_col="gwas.id",
                label_col="gwas.trait",
            ),
            NetworkNodeSchema(
                meta_node="GwasSecondary",
                id_col="assoc_gwas.id",
                label_col="assoc_gwas.trait",
            ),
            NetworkNodeSchema(
                meta_node="Gwas",
                id_col="assoc_gwas2.id",
                label_col="assoc_gwas2.trait",
            ),
        ],
        edges=[
            NetworkEdgeSchema(
                from_col="gwas.id",
                to_col="assoc_gwas.id",
                from_meta_node="Gwas",
                meta_rel="MR_EVE_MR",
                cols=["gwas.id", "assoc_gwas.id", "mr.pval"],
            ),
            # prs
            NetworkEdgeSchema(
                from_col="gwas.id",
                to_col="assoc_gwas2.id",
                from_meta_node="Gwas",
                meta_rel="PRS",
                cols=["gwas.id", "assoc_gwas2.id", "prs1.p"],
            ),
            NetworkEdgeSchema(
                from_col="assoc_gwas2.id",
                to_col="assoc_gwas.id",
                from_meta_node="Gwas",
                meta_rel="PRS",
                cols=["assoc_gwas2.id", "assoc_gwas.id", "prs2.p"],
            ),
            # obs cor
            NetworkEdgeSchema(
                from_col="gwas.id",
                to_col="assoc_gwas2.id",
                from_meta_node="Gwas",
                meta_rel="OBS_COR",
                cols=["gwas.id", "assoc_gwas2.id", "obs_cor1.cor"],
            ),
            NetworkEdgeSchema(
                from_col="assoc_gwas2.id",
                to_col="assoc_gwas.id",
                from_meta_node="Gwas",
                meta_rel="OBS_COR",
                cols=["assoc_gwas2.id", "assoc_gwas.id", "obs_cor2.cor"],
            ),
            # gwas nlp
            NetworkEdgeSchema(
                from_col="gwas.id",
                to_col="assoc_gwas2.id",
                from_meta_node="Gwas",
                meta_rel="GWAS_NLP",
                cols=["gwas.id", "assoc_gwas2.id", "gwas_nlp1.score"],
            ),
            NetworkEdgeSchema(
                from_col="assoc_gwas2.id",
                to_col="assoc_gwas.id",
                from_meta_node="Gwas",
                meta_rel="GWAS_NLP",
                cols=["assoc_gwas2.id", "assoc_gwas.id", "gwas_nlp2.score"],
            ),
        ],
    ),
)
