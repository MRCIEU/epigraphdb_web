from typing import List, Optional

from .pqtl_utils import (
    calc_api_flag_pleio,
    num_to_round,
    query_api_pqtl_cached,
)


def get_full_results(query, method, search_flag) -> str:
    data = query_api_pqtl_cached(
        query=query, rtype=method, pvalue=1.0, searchflag=search_flag
    )
    if method == "mrres":
        res = gen_csv_mrres(data)
    elif method == "sglmr":
        res = gen_csv_sglmr(data)
    elif method == "inst":
        res = gen_csv_inst(data)
    elif method == "sense":
        res = gen_csv_sense(data)
    return res


def format_csv(header: str, rows: List[List[Optional[str]]]) -> str:
    for row in rows:
        result_row = ""
        for cell in row:
            result_row += str(cell) + ","
        result_row = result_row.strip("\t")
        header += result_row + "\n"
    res = header.strip()
    return res


def gen_csv_mrres(data):
    header = (
        ",".join(
            [
                "Protein",
                "Trait",
                "MRBase ID",
                "N SNP",
                "Method",
                "Effect Size",
                "S.E.",
                "p-value",
            ]
        )
        + "\n"
    )
    rows = [
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
        for row in data["results"]
    ]
    res = format_csv(header=header, rows=rows)
    return res


def gen_csv_sglmr(data):
    header = (
        ",".join(
            [
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
        )
        + "\n"
    )
    rows = [
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
        for row in data["results"]
    ]
    res = format_csv(header=header, rows=rows)
    return res


def gen_csv_inst(data):
    header = (
        ",".join(
            [
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
        )
        + "\n"
    )
    rows = [
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
        for row in data["results"]
    ]
    res = format_csv(header=header, rows=rows)
    return res


def gen_csv_sense(data):
    header = (
        ",".join(
            [
                "rsID",
                "Protein",
                "Trait",
                "MRBase ID",
                "SNP reliability",
                "Direction",
                "Steiger p-value",
                "Associated proteins",
                "Colocalisation probability",
                "Outcome SNP",
                "LD Value",
                "Heterogeneity p-value",
            ]
        )
        + "\n"
    )
    rows = [
        [
            row["rsID"],
            row["expID"],
            row["outID"],
            row["outID_mrbase"],
            row["tier"],
            row["direction"],
            row["steiger_pvalue"],
            # ptcount
            calc_api_flag_pleio(row["rsID"], "count"),
            row["coloc_prob"],
            row["outcome_snp"],
            row["ld_check"],
            row["q_pvalue"],
        ]
        for row in data["results"]
    ]
    res = format_csv(header=header, rows=rows)
    return res
