import math

PVAL_THR = 0.000_000_301
COUNT_THR = 1000


def pqtl_highchart(data, method, search_flag):  # noqa:C901
    """Prepares data in the JSON format for Highchat scatter plot"""
    res = {}
    res["topres"] = []
    res["otherres"] = []
    count_others = 0
    if search_flag == "proteins":
        name_field = "outID"
    else:
        name_field = "expID"
    for item in data["results"]:
        if method == "mrres":
            pval = item["pvalue"]
            beta = item["beta"]
            se = item["se"]
        if method == "sglmr":
            pval = item["pvalue_sgl"]
            beta = item["beta_sgl"]
            se = item["se_slg"]
        # PATCH: pval should not be perfectly zero, otherwise y goes to inf
        if pval is not None and pval > 0.0:
            if pval < PVAL_THR:
                res["topres"].append(
                    {
                        "name": item[name_field],
                        "x": round(beta / se, 3),
                        "y": round(-math.log10(pval), 3),
                    }
                )
            else:
                count_others = count_others + 1
                res["otherres"].append(
                    {
                        "name": item[name_field],
                        "x": round(beta / se, 3),
                        "y": round(-math.log10(pval), 3),
                    }
                )
    # Remove results with p-value > 0.05, if > 1100 results
    if count_others > COUNT_THR:
        temp = {}
        temp["otherres"] = []
        temp["topres"] = []
        for item in res["otherres"]:
            if item["y"] > 1.301:
                temp["otherres"].append(item)
        temp["topres"] = res["topres"]
        res = temp
    return res
