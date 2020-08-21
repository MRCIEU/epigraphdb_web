from typing import Any, Dict

from app.funcs.query_processors import (
    NetworkPlotSchemaInput,
    TopicQueryProcessor,
)

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
multi_snp_mr_table_cols = [
    "gene.ensembl_id",
    "gene.name",
    "gwas.id",
    "gwas.trait",
    "r.beta",
    "r.se",
    "r.p",
]
single_snp_mr_table_cols = [
    "gene.ensembl_id",
    "gene.name",
    "gwas.id",
    "gwas.trait",
    "r.beta",
    "r.se",
    "r.p",
    "r.rsid",
]
cols_to_round = ["r.beta", "r.se"]


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
                table_cols=multi_snp_mr_table_cols,
                network_plot_schema=NetworkPlotSchemaInput(
                    node_schemas=node_schemas_multi_snp,
                    edge_schemas=edge_schemas_multi_snp,
                ),
                cypher_diagram_fn=cypher_diagram,
                api_endpoint=multi_snp_api_endpoint,
                cypher_diagram_params=overall_params,
                cols_to_round=cols_to_round,
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
                table_cols=single_snp_mr_table_cols,
                network_plot_schema=NetworkPlotSchemaInput(
                    node_schemas=node_schemas_single_snp,
                    edge_schemas=edge_schemas_single_snp,
                ),
                cypher_diagram_fn=cypher_diagram,
                api_endpoint=single_snp_api_endpoint,
                cypher_diagram_params=overall_params,
                cols_to_round=cols_to_round,
            )
