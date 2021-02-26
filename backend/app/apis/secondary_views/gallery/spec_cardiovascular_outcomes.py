from app.funcs.network_graph import NetworkEdgeSchema, NetworkNodeSchema
from app.utils.meta_graph import gwas_label_formatter, mr_eve_title_formatter

from .graph import GalleryGraph, GalleryQueryType, GallerySchema

cardiovascular_outcomes = GalleryGraph(
    name="cardiovascular_outcomes",
    title="Risk factors to Cardiovascular outcomes",
    description="""
    """.replace(
        "\n", ""
    ),
    # TODO: Update this to genetic cor
    query="""
        MATCH
            (disease_gwas:Gwas)
            <-[mr:MR_EVE_MR]-(risk_factor_gwas:Gwas)-[gwas_to_variant:GWAS_TO_VARIANT]->
            (variant:Variant)-[:VARIANT_TO_GENE]->(gene:Gene)
            <-[:CPIC|:OPENTARGETS_DRUG_TO_TARGET]-(drug:Drug)
        WHERE
            disease_gwas.trait in [
                "Type 2 diabetes",
                "Overweight",
                "Coronary heart disease",
                "Myocardial infarction"
            ]
            AND
            risk_factor_gwas.category = "Risk factor"
            AND
            mr.pval < 1e-05
            AND
            gwas_to_variant.pval < 1e-5
        OPTIONAL MATCH
            (disease_gwas)-[obs_cor:OBS_COR]-(risk_factor_gwas)
        RETURN
            disease_gwas {.id, .trait},
            risk_factor_gwas {.id, .trait},
            variant {.name},
            gene {.name},
            drug {.label},
            obs_cor {.cor},
            mr {.b, .se, .pval, .selection, .method, .moescore}
        ORDER BY mr.pval ;
    """,
    query_type=GalleryQueryType.cypher,
    schema=GallerySchema(
        nodes=[
            NetworkNodeSchema(
                meta_node="GwasPrimary",
                id_col="disease_gwas.id",
                label_formatter=gwas_label_formatter(node_name="disease_gwas"),
            ),
            NetworkNodeSchema(
                meta_node="Gwas",
                id_col="risk_factor_gwas.id",
                label_formatter=gwas_label_formatter(
                    node_name="risk_factor_gwas"
                ),
            ),
            NetworkNodeSchema(meta_node="Variant", id_col="variant.name"),
            NetworkNodeSchema(
                meta_node="Gene", id_col="gene.name", match_node_by="name"
            ),
            NetworkNodeSchema(meta_node="Drug", id_col="drug.label"),
        ],
        edges=[
            NetworkEdgeSchema(
                from_col="risk_factor_gwas.id",
                to_col="disease_gwas.id",
                from_meta_node="Gwas",
                hover_title_formatter=mr_eve_title_formatter(
                    exposure_id="risk_factor_gwas.id",
                    outcome_id="disease_gwas.id",
                    estimate="mr.b",
                    se="mr.se",
                    p="mr.pval",
                    selection="mr.selection",
                    method="mr.method",
                ),
            ),
            # NetworkEdgeSchema(
            #     from_col="risk_factor_gwas.id",
            #     to_col="disease_gwas.id",
            #     cols=["obs_cor.cor"],
            #     from_meta_node="Gwas",
            #     dashes=True,
            #     arrows=False,
            # ),
            NetworkEdgeSchema(
                from_col="risk_factor_gwas.id",
                to_col="variant.name",
                from_meta_node="Default",
                dashes=True,
                arrows=False,
            ),
            NetworkEdgeSchema(
                from_col="variant.name",
                to_col="gene.name",
                from_meta_node="Default",
                dashes=True,
                arrows=False,
            ),
            NetworkEdgeSchema(
                from_col="drug.label",
                to_col="gene.name",
                from_meta_node="Default",
                dashes=True,
                arrows=False,
            ),
        ],
    ),
)
