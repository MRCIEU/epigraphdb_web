from typing import Optional

from app.funcs.cypher_diagram import CypherDiagram, DiagramEdge, DiagramNode


def cypher_diagram(
    xqtl_mode: str,
    exposure_gene: Optional[str],
    outcome_trait: Optional[str],
    variant: Optional[str],
    mr_method: Optional[str],
    qtl_type: Optional[str],
    pval_threshold: float,
):
    if xqtl_mode == "multi_snp_mr":
        diagram_nodes = [
            DiagramNode(id=1, meta_node="Gene", sub_label=exposure_gene),
            DiagramNode(id=2, meta_node="Gwas", sub_label=outcome_trait),
        ]
        diagram_edges = [
            DiagramEdge(
                from_id=1,
                to_id=2,
                meta_rel="XQTL_MULTI_SNP_MR",
                sub_label=f"p < {pval_threshold}\n{mr_method}\n{qtl_type}",
            )
        ]
    else:
        diagram_nodes = [
            DiagramNode(id=1, meta_node="Gene", sub_label=exposure_gene),
            DiagramNode(id=2, meta_node="Gwas", sub_label=outcome_trait),
            DiagramNode(id=3, meta_node="Variant", sub_label=variant),
        ]
        diagram_edges = [
            DiagramEdge(
                from_id=1,
                to_id=2,
                meta_rel="XQTL_SINGLE_SNP_MR_GENE_GWAS",
                sub_label=f"p < {pval_threshold}\n{qtl_type}",
            ),
            DiagramEdge(
                from_id=3, to_id=1, meta_rel="XQTL_SINGLE_SNP_MR_SNP_GENE"
            ),
        ]
    diagram = CypherDiagram(nodes=diagram_nodes, edges=diagram_edges)
    diagram_data = diagram.generate_diagram()
    return diagram_data
