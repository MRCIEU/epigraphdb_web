import numpy as np
import pandas as pd

from app.utils.data_table import ROUNDING, process_table_data

# bf corrected pval threshold
PVAL_THRESHOLD = 1.1e-6


def process_data(data):
    """Process upstream covid xqtl data and add plots
    """

    table_data = None
    plot_data = None
    if len(data) > 0:
        df = pd.json_normalize(data)
        table_data = process_table_data(df=df, cols_to_round=["b", "se"])
        plot_data = process_volcano_plot(df=df)
    res = {"table_data": table_data, "plot_data": plot_data}
    return res


def process_volcano_plot(df: pd.DataFrame):
    res_df = (
        df[["outcome_trait", "exposure_gene_name", "tissue", "b", "se", "p"]]
        .assign(z_score=lambda df: df["b"] / df["se"])
        .assign(neg_log10_pval=lambda df: -np.log10(df["p"]))
        .round({"z_score": ROUNDING, "neg_log10_pval": ROUNDING})
        .assign(
            x=lambda df: df["z_score"],
            y=lambda df: df["neg_log10_pval"],
            outcome=lambda df: df["outcome_trait"],
            exposure=lambda df: df["exposure_gene_name"],
            tissue=lambda df: df["tissue"],
        )
        .assign(
            group=lambda df: df["p"].apply(
                lambda x: "top_results"
                if x < PVAL_THRESHOLD
                else "other_results"
            )
        )
    )
    other_res = res_df.query("group == 'other_results'")[
        ["outcome", "exposure", "tissue", "x", "y"]
    ].to_dict(orient="records")
    top_res = []
    if len(res_df.query("group == 'top_results'")) > 0:
        top_res = res_df.query("group == 'top_results'")[
            ["outcome", "exposure", "tissue", "x", "y"]
        ].to_dict(orient="records")
    res = {"top_results": top_res, "other_results": other_res}
    return res
