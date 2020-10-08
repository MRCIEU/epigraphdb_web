from .calc_flag_sensitivity import calc_flag_sensitivity
from .pqtl_aggregate_results import pqtl_aggregate_results
from .pqtl_highchart import pqtl_highchart
from .pqtl_network_plot import pqtl_network_plot
from .pqtl_table import pqtl_format_table
from .pqtl_utils import (
    calc_api_flag_pleio,
    calc_flag_hetero,
    num_to_round,
    query_api_pqtl_cached,
)

PVALUE_THR_PROTEINS = 1.00
PVALUE_THR_NON_PROTEINS = 0.05


def pqtl_main(query, method, search_flag, overwrite: bool = False):
    """Returns the table of results,
    i.e. (MR, sensitivity analyses, SNP-info),
    per the query type ('method')
    and search entity ('searchtype'), i.e. 'proteins' or 'traits'
    """
    hierarchy: bool = False
    if search_flag == "proteins":
        pvalue_thr = PVALUE_THR_PROTEINS
    else:
        pvalue_thr = PVALUE_THR_NON_PROTEINS
    if method not in ["simple", "mrres", "sglmr", "inst", "sense"]:
        raise
    if method == "simple":
        (
            pqtl_results,
            plot_output,
            headers,
            result_table,
            count,
        ) = pqtl_main_simple(
            query=query,
            pvalue_thr=pvalue_thr,
            search_flag=search_flag,
            overwrite=overwrite,
        )
    elif method == "mrres":
        (
            pqtl_results,
            plot_output,
            headers,
            result_table,
            count,
        ) = pqtl_main_mrres(
            query=query,
            pvalue_thr=pvalue_thr,
            search_flag=search_flag,
            overwrite=overwrite,
        )
    elif method == "sglmr":
        (
            pqtl_results,
            plot_output,
            headers,
            result_table,
            count,
        ) = pqtl_main_sglmr(
            query=query,
            pvalue_thr=pvalue_thr,
            search_flag=search_flag,
            overwrite=overwrite,
        )
    elif method == "inst":
        (
            pqtl_results,
            plot_output,
            headers,
            result_table,
            count,
        ) = pqtl_main_inst(
            query=query,
            pvalue_thr=pvalue_thr,
            search_flag=search_flag,
            overwrite=overwrite,
        )
        hierarchy = True
    elif method == "sense":
        (
            pqtl_results,
            plot_output,
            headers,
            result_table,
            count,
        ) = pqtl_main_sense(
            query=query,
            pvalue_thr=pvalue_thr,
            search_flag=search_flag,
            overwrite=overwrite,
        )
        hierarchy = True

    if count > 12:
        hierarchy = False
    no_results: bool = False
    if len(result_table) == 0:
        no_results = True

    table_output = pqtl_format_table(headers=headers, table_data=result_table)
    res = {
        "table_output": table_output,
        "plot_output": plot_output,
        "no_results": no_results,
        "hierarchy": hierarchy,
        "search_flag": search_flag,
    }
    return res


def pqtl_main_simple(query, pvalue_thr, search_flag, overwrite: bool = False):
    pqtl_results = query_api_pqtl_cached(
        query=query,
        rtype="simple",
        pvalue=pvalue_thr,
        searchflag=search_flag,
        overwrite=overwrite,
    )
    plot_output = pqtl_network_plot(
        data=pqtl_results, method="simple", search_flag=search_flag
    )
    headers = [
        "Protein",
        "Trait",
        "MRBase ID",
        "Protein associates with trait",
        "Low heterogeneity",
        "rsID",
        "Cis acting instrument",
        "Correct causal direction",
        "Instrument associates with one protein",
        "Shared causal variant",
    ]

    result_table = []
    count = 0
    for row in pqtl_results["results"]:
        count = count + 1
        stg_flag, coloc_flag = calc_flag_sensitivity(
            row["direction"],
            row["steiger_pvalue"],
            row["coloc_prob"],
            row["pvalue"],
            row["ld_check"],
        )
        consist_flag = calc_flag_hetero(row["q_pvalue"])
        ptcount = calc_api_flag_pleio(row["rsID"], "count")
        result_table.append(
            [
                row["expID"],
                row["outID"],
                row["outID_mrbase"],
                row["pvalue"],
                consist_flag,
                row["rsID"],
                row["trans_cis"],
                stg_flag,
                ptcount,
                coloc_flag,
            ]
        )

    results = pqtl_aggregate_results(result_table, search_flag)
    result_table = results

    return pqtl_results, plot_output, headers, result_table, count


def pqtl_main_mrres(query, pvalue_thr, search_flag, overwrite: bool = False):
    pqtl_results = query_api_pqtl_cached(
        query=query,
        rtype="mrres",
        pvalue=pvalue_thr,
        searchflag=search_flag,
        overwrite=overwrite,
    )
    plot_output = pqtl_highchart(
        data=pqtl_results, method="mrres", search_flag=search_flag
    )
    headers = [
        "Protein",
        "Trait",
        "MRBase ID",
        "N SNP",
        "Method",
        "Effect Size",
        "S.E.",
        "p-value",
    ]

    result_table = []
    count = 0
    for row in pqtl_results["results"]:
        count = count + 1
        result_table.append(
            [
                row["expID"],
                row["outID"],
                row["outID_mrbase"],
                row["nsnp"],
                row["method"],
                num_to_round(row["beta"], 4),
                num_to_round(row["se"], 4),
                row["pvalue"],
            ]
        )

    return pqtl_results, plot_output, headers, result_table, count


def pqtl_main_sglmr(query, pvalue_thr, search_flag, overwrite: bool = False):
    pqtl_results = query_api_pqtl_cached(
        query=query,
        rtype="sglmr",
        pvalue=pvalue_thr,
        searchflag=search_flag,
        overwrite=overwrite,
    )
    plot_output = pqtl_highchart(
        data=pqtl_results, method="sglmr", search_flag=search_flag
    )
    headers = [
        "rsID",
        "Protein",
        "Trait",
        "MRBase ID",
        "SNP reliability",
        "Effect Size",
        "S.E.",
        "p-value",
        "Cis Trans",
    ]

    result_table = []
    count = 0
    for row in pqtl_results["results"]:
        count = count + 1
        result_table.append(
            [
                row["rsID"],
                row["expID"],
                row["outID"],
                row["outID_mrbase"],
                row["tier"],
                num_to_round(row["beta_sgl"], 4),
                num_to_round(row["se_slg"], 4),
                row["pvalue_sgl"],
                row["trans_cis"],
            ]
        )

    return pqtl_results, plot_output, headers, result_table, count


def pqtl_main_inst(query, pvalue_thr, search_flag, overwrite: bool = False):
    pqtl_results = query_api_pqtl_cached(
        query=query,
        rtype="inst",
        pvalue=pvalue_thr,
        searchflag=search_flag,
        overwrite=overwrite,
    )
    plot_output = pqtl_network_plot(
        data=pqtl_results, method="inst", search_flag=search_flag
    )
    headers = [
        "rsID",
        "Protein",
        "Trait",
        "MRBase ID",
        "EA",
        "NEA",
        "EAF",
        "Cis Trans",
        "N Exposure",
        "N Outcome",
        "Study Exposure",
        "Study Outcome",
    ]

    result_table = []
    count = 0
    for row in pqtl_results["results"]:
        count = count + 1
        result_table.append(
            [
                row["rsID"],
                row["expID"],
                row["outID"],
                row["outID_mrbase"],
                row["ea"],
                row["nea"],
                num_to_round(row["eaf_exp"], 4),
                row["trans_cis"],
                row["sample_exp"],
                row["sample_out"],
                row["author_exp"],
                row["author_out"],
            ]
        )

    return pqtl_results, plot_output, headers, result_table, count


def pqtl_main_sense(query, pvalue_thr, search_flag, overwrite: bool = False):
    pqtl_results = query_api_pqtl_cached(
        query=query,
        rtype="sense",
        pvalue=pvalue_thr,
        searchflag=search_flag,
        overwrite=overwrite,
    )
    plot_output = pqtl_network_plot(
        data=pqtl_results, method="sense", search_flag=search_flag
    )
    headers = [
        "rsID",
        "Protein",
        "Trait",
        "MRBase ID",
        "SNP reliability",
        "Direction",
        "Steiger p-value",
        "Associated proteins",
        "Post. prob. colocalization",
        "Outcome SNP",
        "LD Value",
        "Heterogeneity p-value",
    ]

    result_table = []
    count = 0
    for row in pqtl_results["results"]:
        count = count + 1
        ptlist = calc_api_flag_pleio(row["rsID"], "proteins")
        result_table.append(
            [
                row["rsID"],
                row["expID"],
                row["outID"],
                row["outID_mrbase"],
                row["tier"],
                row["direction"],
                row["steiger_pvalue"],
                ptlist,
                row["coloc_prob"],
                row["outcome_snp"],
                row["ld_check"],
                row["q_pvalue"],
            ]
        )

    return pqtl_results, plot_output, headers, result_table, count
