from app.funcs.network_graph import NetworkEdgeSchema, NetworkNodeSchema
from app.utils.meta_graph import gwas_label_formatter, mr_eve_title_formatter

from .graph import GalleryGraph, GalleryQueryType, GallerySchema

drugs_coronary_heart_disease = GalleryGraph(
    name="drugs_coronary_heart_disease",
    title="Drugs: Coronary heart disease",
    description="""
        <p>
        Evidence of potential drugs for a disease outcome
        (e.g Coronary heart disease) via SNPs that influence
        causal risk factors for that outcome.
        </p>

        <p>
        Visit <a href='http://epigraphdb.org/risk-factor-drugs/'>
        http://epigraphdb.org/risk-factor-drugs/</a>
        for more details.
        </p>
    """.replace(
        "\n", ""
    ),
    # TODO: genetic cor
    query="""
        MATCH
            (trait:Gwas {trait: "Coronary heart disease"})
            <-[mr:MR]-(assoc_trait:Gwas)-[gwas_to_variant:GWAS_TO_VARIANT]->
            (variant:Variant)-[:VARIANT_TO_GENE]->(gene:Gene)
            <-[:CPIC|:OPENTARGETS_DRUG_TO_TARGET]-(drug:Drug)
        WHERE
            trait.trait <> assoc_trait.trait AND
            mr.pval < 1e-05 AND
            gwas_to_variant.pval < 1e-8
        RETURN
            trait {.id, .trait},
            assoc_trait {.id, .trait},
            variant {.name},
            gene {.name},
            drug {.label},
            mr {.b, .se, .pval, .selection, .method, .moescore}
        ORDER BY mr.pval ;
    """,
    query_type=GalleryQueryType.cypher,
    schema=GallerySchema(
        nodes=[
            NetworkNodeSchema(
                meta_node="GwasExposure",
                id_col="trait.id",
                label_formatter=gwas_label_formatter(node_name="trait"),
            ),
            NetworkNodeSchema(
                meta_node="Gwas",
                id_col="assoc_trait.id",
                label_formatter=gwas_label_formatter(node_name="assoc_trait"),
            ),
            NetworkNodeSchema(meta_node="Variant", id_col="variant.name"),
            NetworkNodeSchema(
                meta_node="Gene", id_col="gene.name", match_node_by="name"
            ),
            NetworkNodeSchema(meta_node="Drug", id_col="drug.label"),
        ],
        edges=[
            NetworkEdgeSchema(
                from_col="assoc_trait.id",
                to_col="trait.id",
                from_meta_node="Gwas",
                hover_title_formatter=mr_eve_title_formatter(
                    exposure_id="assoc_trait.id",
                    outcome_id="trait.id",
                    estimate="mr.b",
                    se="mr.se",
                    p="mr.pval",
                    selection="mr.selection",
                    method="mr.method",
                ),
            ),
            NetworkEdgeSchema(
                from_col="assoc_trait.id",
                to_col="variant.name",
                from_meta_node="Variant",
            ),
            NetworkEdgeSchema(
                from_col="variant.name",
                to_col="gene.name",
                from_meta_node="Variant",
            ),
            NetworkEdgeSchema(
                from_col="drug.label",
                to_col="gene.name",
                from_meta_node="Drug",
            ),
        ],
    ),
)
