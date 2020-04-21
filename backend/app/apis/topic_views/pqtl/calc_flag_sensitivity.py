from typing import Optional, Tuple

COLOC_THR = 0.8
PVALUE_THR = 0.00001
STEIGER_PVALUE_THR = 0.05


def calc_flag_sensitivity(
    steiger: str,
    steiger_p: float,
    coloc: Optional[float],
    pvalue: float,
    ld_score: Optional[float],
) -> Tuple[str, str]:
    """Estimates whether the sensitivity analyses were passed
    for a pair <exposure,outcome>
    """
    stg = "NA"
    coloc_pr = "NA"
    if coloc is not None:
        stg, coloc_pr = calc_flag_coloc(
            steiger=steiger, steiger_p=steiger_p, coloc=coloc, pvalue=pvalue
        )
    elif ld_score is not None and coloc is None:
        stg, coloc_pr = calc_flag_ld_score(
            steiger=steiger,
            steiger_p=steiger_p,
            pvalue=pvalue,
            ld_score=ld_score,
        )
    else:
        if (
            steiger == "TRUE"
            and steiger_p < STEIGER_PVALUE_THR
            and pvalue < PVALUE_THR
        ):
            stg = "Yes"
            coloc_pr = "NA"
        elif (
            steiger == "FALSE"
            and steiger_p < STEIGER_PVALUE_THR
            and pvalue < PVALUE_THR
        ):
            stg = "No"
            coloc_pr = "NA"
    return stg, coloc_pr


def calc_flag_coloc(
    steiger: str, steiger_p: float, coloc: float, pvalue: float
) -> Tuple[str, str]:
    """when coloc is not None
    """
    stg = "NA"
    coloc_pr = "NA"
    if coloc > COLOC_THR:
        if (
            steiger == "TRUE"
            and steiger_p < STEIGER_PVALUE_THR
            and pvalue < PVALUE_THR
        ):
            stg = "Yes"
            coloc_pr = "Yes"
        elif (
            steiger == "FALSE"
            and steiger_p < STEIGER_PVALUE_THR
            and pvalue < PVALUE_THR
        ):
            stg = "No"
            coloc_pr = "Yes"
        else:
            stg = "NA"
            coloc_pr = "Yes"
    elif coloc < COLOC_THR:
        if (
            steiger == "TRUE"
            and steiger_p < STEIGER_PVALUE_THR
            and pvalue < PVALUE_THR
        ):
            stg = "Yes"
            coloc_pr = "No"
        elif (
            steiger == "FALSE"
            and steiger_p < STEIGER_PVALUE_THR
            and pvalue < PVALUE_THR
        ):
            stg = "No"
            coloc_pr = "No"
        else:
            stg = "NA"
            coloc_pr = "No"
    return stg, coloc_pr


def calc_flag_ld_score(
    steiger: str, steiger_p: float, pvalue: float, ld_score: float
) -> Tuple[str, str]:
    """when ld_score is not None and coloc is none
    """
    stg = "NA"
    coloc_pr = "NA"
    if ld_score > COLOC_THR:
        if (
            steiger == "TRUE"
            and steiger_p < STEIGER_PVALUE_THR
            and pvalue < PVALUE_THR
        ):
            stg = "Yes"
            coloc_pr = "Yes"
        elif (
            steiger == "FALSE"
            and steiger_p < STEIGER_PVALUE_THR
            and pvalue < PVALUE_THR
        ):
            stg = "No"
            coloc_pr = "Yes"
        else:
            stg = "NA"
            coloc_pr = "Yes"
    elif ld_score < COLOC_THR:
        if (
            steiger == "TRUE"
            and steiger_p < STEIGER_PVALUE_THR
            and pvalue < PVALUE_THR
        ):
            stg = "Yes"
            coloc_pr = "No"
        elif (
            steiger == "FALSE"
            and steiger_p < STEIGER_PVALUE_THR
            and pvalue < PVALUE_THR
        ):
            stg = "No"
            coloc_pr = "No"
        else:
            stg = "NA"
            coloc_pr = "No"
    return stg, coloc_pr
