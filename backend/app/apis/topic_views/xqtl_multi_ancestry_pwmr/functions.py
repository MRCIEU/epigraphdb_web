import numpy as np
import pandas as pd

from app.utils.data_table import ROUNDING, process_table_data

# # bf corrected pval threshold
# PVAL_THRESHOLD = 1.1e-6


def process_data(data):
    """Process upstream xqtl_pwas data and add plots"""

    table_data = None
    plot_data = None
    if len(data) > 0:
        df = pd.DataFrame(data)
        table_data = process_table_data(df=df, cols_to_round=["b", "se"])
        plot_data = process_volcano_plot(df=df)
    res = {"table_data": table_data, "plot_data": plot_data}
    return res


def process_volcano_plot(df: pd.DataFrame):
    res_df = (
        df[["gwas_name", "gene_name", "ancestry", "b", "se", "pval"]]
        # NOTE: there are cases with extremely low pvals
        # .query("pval > 1e-20")
        .query("pval > 0")
        .assign(pval=lambda df: df["pval"].astype(float))
        .assign(z_score=lambda df: df["b"] / df["se"])
        .assign(neg_log10_pval=lambda df: -np.log10(df["pval"]))
        .round({"z_score": ROUNDING, "neg_log10_pval": ROUNDING})
        .assign(
            x=lambda df: df["z_score"],
            y=lambda df: df["neg_log10_pval"],
            outcome=lambda df: df["gwas_name"],
            exposure=lambda df: df["gene_name"],
        )
    )
    res = res_df[["outcome", "exposure", "ancestry", "x", "y"]].to_dict(
        orient="records"
    )
    return res
