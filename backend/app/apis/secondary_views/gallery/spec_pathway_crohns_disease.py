from app.funcs.network_graph import NetworkEdgeSchema, NetworkNodeSchema
from app.utils.meta_graph import gwas_label_formatter

from .graph import GalleryGraph, GalleryQueryType, GallerySchema

pathway_crohns_disease = GalleryGraph(
    name="pathway_crohns_disease",
    title="Pathway: Crohn's disease",
    description="""
        <p>
        Common pathways and pleiotropic relationships via
        trait-snp-gene-protein-pathway.
        </p>

        <p>
        Visit <a href='http://epigraphdb.org/pathway/'>
        http://epigraphdb.org/pathway/</a>
        for more details.
        </p>
    """.replace(
        "\n", ""
    ),
    query="""
        MATCH
            (gwas:Gwas {trait: "Crohn's disease"})
            -[gwas_to_variant:GWAS_TO_VARIANT]->(variant:Variant)-[variant_to_gene:VARIANT_TO_GENE]->
            (gene:Gene)-[gene_to_protein:GENE_TO_PROTEIN]->(protein:Protein)
            -[protein_in_pathway:PROTEIN_IN_PATHWAY]->(pathway:Pathway)
        WHERE
            gwas_to_variant.pval < 1e-05 AND
            variant.name is not null AND
            gene.name is not null
        RETURN
            gwas {.id, .trait},
            gwas_to_variant {.se, .pval, .samplesize, .beta},
            variant {.name},
            gene {.name},
            protein {.uniprot_id},
            pathway {.reactome_id, .name}
        ORDER BY gwas_to_variant.pval ;
    """,
    query_type=GalleryQueryType.cypher,
    schema=GallerySchema(
        nodes=[
            NetworkNodeSchema(
                meta_node="Gwas",
                id_col="gwas.id",
                label_formatter=gwas_label_formatter(),
            ),
            NetworkNodeSchema(
                meta_node="Variant",
                id_col="variant.name",
                label_col="variant.name",
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
        ],
        edges=[
            NetworkEdgeSchema(
                from_col="gwas.id",
                to_col="variant.name",
                from_meta_node="Gwas",
                hover_title_formatter=lambda row: """
                            <b>gwas.id</b>: {gwas_id},
                            <b>variant.name</b>: {variant_name}</br>
                            <b>beta</b>: {beta:.2E},
                            <b>se</b>: {se:.2E},
                            <b>p</b>: {p:.2E}
                            """.format(
                    gwas_id=row["gwas.id"],
                    variant_name=row["variant.name"],
                    beta=row["gwas_to_variant.beta"],
                    se=row["gwas_to_variant.se"],
                    p=row["gwas_to_variant.pval"],
                ),
            ),
            NetworkEdgeSchema(
                from_col="variant.name",
                to_col="gene.name",
                from_meta_node="Variant",
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
        ],
    ),
)
