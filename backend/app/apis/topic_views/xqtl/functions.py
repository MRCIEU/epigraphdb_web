from typing import Any, Dict

from app.funcs.query_processors import (
    NetworkPlotSchemaInput,
    TopicQueryProcessor,
)
from app.utils.data_table import NodeCol, RelCol

from .diagram import cypher_diagram
from .graph import (
    edge_schemas_multi_snp,
    edge_schemas_single_snp,
    node_schemas_multi_snp,
    node_schemas_single_snp,
)

multi_snp_master_name = "xqtl_multi_snp"
single_snp_master_name = "xqtl_single_snp"
multi_snp_api_endpoint = "xqtl/multi-snp-mr"
single_snp_api_endpoint = "xqtl/single-snp-mr"
GENE_DESC = ""
GWAS_DESC = ""
XQTL_SINGLE_SNP_MR_DESC = ""
XQTL_MULTI_SNP_MR_DESC = ""
multi_snp_mr_table_col_configs = {
    "gene.ensembl_id": NodeCol("Gene", "ensembl_id", GENE_DESC),
    "gene.name": NodeCol("Gene", "name", GENE_DESC),
    "gwas.id": NodeCol("Gwas", "id", GWAS_DESC),
    "gwas.trait": NodeCol("Gwas", "trait", GWAS_DESC),
    "r.beta": RelCol(
        "XQTL_MULTI_SNP_MR", "beta", XQTL_MULTI_SNP_MR_DESC, rounding=True
    ),
    "r.se": RelCol(
        "XQTL_MULTI_SNP_MR", "se", XQTL_MULTI_SNP_MR_DESC, rounding=True
    ),
    "r.p": RelCol("XQTL_MULTI_SNP_MR", "p", XQTL_MULTI_SNP_MR_DESC),
}
single_snp_mr_table_col_configs = {
    "gene.ensembl_id": NodeCol("Gene", "ensembl_id", GENE_DESC),
    "gene.name": NodeCol("Gene", "name", GENE_DESC),
    "gwas.id": NodeCol("Gwas", "id", GWAS_DESC),
    "gwas.trait": NodeCol("Gwas", "trait", GWAS_DESC),
    "r.beta": RelCol(
        "XQTL_SINGLE_SNP_MR_GENE_GWAS",
        "beta",
        XQTL_SINGLE_SNP_MR_DESC,
        rounding=True,
    ),
    "r.se": RelCol(
        "XQTL_SINGLE_SNP_MR_GENE_GWAS",
        "se",
        XQTL_SINGLE_SNP_MR_DESC,
        rounding=True,
    ),
    "r.p": RelCol(
        "XQTL_SINGLE_SNP_MR_GENE_GWAS", "p", XQTL_SINGLE_SNP_MR_DESC
    ),
    "r.rsid": RelCol(
        "XQTL_SINGLE_SNP_MR_GENE_GWAS", "rsid", XQTL_SINGLE_SNP_MR_DESC
    ),
}


class XqtlQueryProcessor(TopicQueryProcessor):
    def __init__(self, params: Dict[str, Any]):
        overall_params = {
            "xqtl_mode": params["xqtl_mode"],
            "exposure_gene": params["exposure_gene"],
            "outcome_trait": params["outcome_trait"],
            "variant": params["variant"],
            "mr_method": params["mr_method"],
            "qtl_type": params["qtl_type"],
            "pval_threshold": params["pval_threshold"],
        }
        if overall_params["xqtl_mode"] == "multi_snp_mr":
            input_params = {
                "exposure_gene": params["exposure_gene"],
                "outcome_trait": params["outcome_trait"],
                "mr_method": params["mr_method"],
                "qtl_type": params["qtl_type"],
                "pval_threshold": params["pval_threshold"],
            }
            super().__init__(
                master_name=multi_snp_master_name,
                params=input_params,
                table_col_configs=multi_snp_mr_table_col_configs,
                network_plot_schema=NetworkPlotSchemaInput(
                    node_schemas=node_schemas_multi_snp,
                    edge_schemas=edge_schemas_multi_snp,
                ),
                cypher_diagram_fn=cypher_diagram,
                api_endpoint=multi_snp_api_endpoint,
                cypher_diagram_params=overall_params,
            )
        else:
            input_params = {
                "exposure_gene": params["exposure_gene"],
                "outcome_trait": params["outcome_trait"],
                "variant": params["variant"],
                "qtl_type": params["qtl_type"],
                "pval_threshold": params["pval_threshold"],
            }
            super().__init__(
                master_name=single_snp_master_name,
                params=input_params,
                table_col_configs=single_snp_mr_table_col_configs,
                network_plot_schema=NetworkPlotSchemaInput(
                    node_schemas=node_schemas_single_snp,
                    edge_schemas=edge_schemas_single_snp,
                ),
                cypher_diagram_fn=cypher_diagram,
                api_endpoint=single_snp_api_endpoint,
                cypher_diagram_params=overall_params,
            )
