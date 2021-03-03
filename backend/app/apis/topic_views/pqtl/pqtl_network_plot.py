import copy

import numpy as np

COLOC_THR = 0.8
PVALUE_THR_PROTEINS = 0.05
PVALUE_THR_NON_PROTEINS = 0.01
PVALUE_THR_SGL = 0.001
PVALUE_THR_STEIGER = 0.05
GENECARDS_URL = "https://www.genecards.org/Search/Keyword?queryString=%s"
SNP_URL = "https://www.ncbi.nlm.nih.gov/snp/?term=%s"


def pqtl_network_plot(data, method, search_flag):
    """Prepares data in the JSON format for vis.js network visualisation"""
    res = {"nodes": [], "links": []}
    # records what entities have been registered
    nodes = []
    if search_flag == "proteins":
        pvalue_thr = PVALUE_THR_PROTEINS
    else:
        pvalue_thr = PVALUE_THR_NON_PROTEINS
    plot_data = copy.deepcopy(data)
    for item in plot_data["results"]:
        res, nodes = pqtl_network_plot_init(
            item=item,
            res=res,
            nodes=nodes,
            method=method,
            search_flag=search_flag,
            pvalue_thr=pvalue_thr,
        )
        if method == "mrres" or method == "simple":
            res, nodes = pqtl_network_plot_mrres_simple(
                item=item, res=res, nodes=nodes, search_flag=search_flag
            )
        if method == "inst" or method == "sglmr":
            res, nodes = pqtl_network_plot_inst_sglmr(
                item=item,
                res=res,
                nodes=nodes,
                search_flag=search_flag,
                pvalue_thr=pvalue_thr,
            )
        if method == "sense":
            res, nodes = pqtl_network_plot_sense(
                item=item,
                res=res,
                nodes=nodes,
                search_flag=search_flag,
                pvalue_thr=pvalue_thr,
            )
        reslinks = []
        for item in res["links"]:
            if item not in reslinks:
                reslinks.append(item)
        res["links"] = reslinks
    return res


def pqtl_network_plot_init(item, res, nodes, method, search_flag, pvalue_thr):
    if "coloc_prob" in item and item["coloc_prob"] is None:
        # HACKY PATCH:
        # Allow comparison of missing (NoneType) data
        item["coloc_prob"] = np.nan
    if (
        search_flag != "proteins"
        and item["pvalue"] is not None
        and item["expID"] not in nodes
        and float(item["pvalue"]) < pvalue_thr
    ):
        url = GENECARDS_URL % (item["expID"])
        res["nodes"].append(
            {
                "id": item["expID"],
                "label": item["expID"],
                "group": "expo",
                "shape": "box",
                "level": 2,
                "url": url,
            }
        )
        nodes.append(item["expID"])
    elif item["expID"] not in nodes:
        url = GENECARDS_URL % (item["expID"])
        res["nodes"].append(
            {
                "id": item["expID"],
                "label": item["expID"],
                "group": "expo",
                "shape": "box",
                "level": 2,
                "url": url,
            }
        )
        nodes.append(item["expID"])
    if (
        method != "sglmr"
        and item["pvalue"] is not None
        and item["outID_mrbase"] not in nodes
        and float(item["pvalue"]) < pvalue_thr
    ):
        s = item["outID"]
        res["nodes"].append(
            {
                "id": item["outID_mrbase"],
                "label": s[0:12],
                "title": item["outID"],
                "group": "out",
                "shape": "box",
                "level": 3,
            }
        )
        nodes.append(item["outID_mrbase"])
    elif (
        "pvalue_sgl" in item
        and item["pvalue_sgl"] is not None
        and item["outID_mrbase"] not in nodes
        and float(item["pvalue_sgl"]) < PVALUE_THR_SGL
    ):
        s = item["outID"]
        res["nodes"].append(
            {
                "id": item["outID_mrbase"],
                "label": s[0:12],
                "title": item["outID"],
                "group": "out",
                "shape": "box",
                "level": 3,
            }
        )
        nodes.append(item["outID_mrbase"])
    return res, nodes


def pqtl_network_plot_mrres_simple(item, res, nodes, search_flag):
    res["links"].append(
        {
            "from": item["expID"],
            "to": item["outID_mrbase"],
            "arrows": "to",
            "value": int(abs(item["beta"] / item["se"]) * 10) + 1,
            "arrowStrikethrough": "true",
            "color": {
                "color": "#f3b499",
                "highlight": "#f3b499",
                "hover": "#f3b499",
            },
            "title": str(round(item["beta"] / item["se"], 2)),
        }
    )
    return res, nodes


def pqtl_network_plot_inst_sglmr(item, res, nodes, search_flag, pvalue_thr):
    if search_flag == "proteins":
        if item["rsID"] not in nodes:
            url = SNP_URL % item["rsID"]
            if item["trans_cis"] == "cis":
                res["nodes"].append(
                    {
                        "id": item["rsID"],
                        "label": item["rsID"],
                        "group": "snp_cis",
                        "level": 1,
                        "url": url,
                    }
                )
            else:
                res["nodes"].append(
                    {
                        "id": item["rsID"],
                        "label": item["rsID"],
                        "group": "snp_trans",
                        "shape": "box",
                        "level": 1,
                        "url": url,
                    }
                )
            nodes.append(item["rsID"])
    elif item["pvalue"] is not None:
        if item["rsID"] not in nodes and float(item["pvalue"]) < pvalue_thr:
            url = SNP_URL % item["rsID"]
            if item["trans_cis"] == "cis":
                res["nodes"].append(
                    {
                        "id": item["rsID"],
                        "label": item["rsID"],
                        "group": "snp_cis",
                        "level": 1,
                        "url": url,
                    }
                )
            else:
                res["nodes"].append(
                    {
                        "id": item["rsID"],
                        "label": item["rsID"],
                        "group": "snp_trans",
                        "shape": "box",
                        "level": 1,
                        "url": url,
                    }
                )
            nodes.append(item["rsID"])
    res["links"].append(
        {"from": item["rsID"], "to": item["expID"], "color": {"inherit": "to"}}
    )
    res["links"].append({"from": item["expID"], "to": item["outID_mrbase"]})
    res["links"].append(
        {
            "from": item["rsID"],
            "to": item["outID_mrbase"],
            "dashes": "true",
            "color": {"inherit": "to"},
        }
    )
    return res, nodes


def pqtl_network_plot_sense(  # noqa:C901
    item, res, nodes, search_flag, pvalue_thr
):
    if search_flag == "proteins":
        if item["rsID"] not in nodes:
            url = SNP_URL % item["rsID"]
            if item["trans_cis"] == "cis":
                res["nodes"].append(
                    {
                        "id": item["rsID"],
                        "label": item["rsID"],
                        "group": "snp_cis",
                        "level": 1,
                        "url": url,
                    }
                )
            else:
                res["nodes"].append(
                    {
                        "id": item["rsID"],
                        "label": item["rsID"],
                        "group": "snp_trans",
                        "shape": "box",
                        "level": 1,
                        "url": url,
                    }
                )
            nodes.append(item["rsID"])
    else:
        if item["pvalue"] is not None:
            if (
                item["rsID"] not in nodes
                and float(item["pvalue"]) < pvalue_thr
            ):
                url = SNP_URL % item["rsID"]
                if item["trans_cis"] == "cis":
                    res["nodes"].append(
                        {
                            "id": item["rsID"],
                            "label": item["rsID"],
                            "group": "snp_cis",
                            "level": 1,
                            "url": url,
                        }
                    )
                else:
                    res["nodes"].append(
                        {
                            "id": item["rsID"],
                            "label": item["rsID"],
                            "group": "snp_trans",
                            "shape": "box",
                            "level": 1,
                            "url": url,
                        }
                    )
                nodes.append(item["rsID"])
    if (
        item["direction"] == "TRUE"
        and item["steiger_pvalue"] < PVALUE_THR_STEIGER
        and item["coloc_prob"] > COLOC_THR
    ):
        res["links"].append(
            {
                "from": item["rsID"],
                "to": item["expID"],
                "arrows": "to",
                "color": {"color": "gray"},
            }
        )
        res["links"].append(
            {
                "from": item["expID"],
                "to": item["outID_mrbase"],
                "arrows": "to",
                "title": item["rsID"] + ": coloc (pass); direction (pass)",
                "color": {
                    "color": "green",
                    "highlight": "green",
                    "hover": "green",
                },
            }
        )
        res["links"].append(
            {
                "from": item["rsID"],
                "to": item["outID_mrbase"],
                "dashes": "true",
                "title": "NA",
                "color": {"color": "gray"},
            }
        )
    elif (
        item["direction"] == "TRUE"
        and item["steiger_pvalue"] < PVALUE_THR_STEIGER
        and item["coloc_prob"] < COLOC_THR
    ):
        res["links"].append(
            {
                "from": item["rsID"],
                "to": item["expID"],
                "arrows": "to",
                "color": {"color": "gray"},
            }
        )
        res["links"].append(
            {
                "from": item["expID"],
                "to": item["outID_mrbase"],
                "arrows": "to",
                "title": item["rsID"] + ": coloc (fail); direction (pass)",
                "color": {"color": "red", "highlight": "red", "hover": "red"},
            }
        )
        res["links"].append(
            {
                "from": item["rsID"],
                "to": item["outID_mrbase"],
                "dashes": "true",
                "title": "NA",
                "color": {"color": "gray"},
            }
        )
    elif (
        item["direction"] == "FALSE"
        and item["steiger_pvalue"] < PVALUE_THR_STEIGER
        and item["coloc_prob"] > COLOC_THR
    ):
        res["links"].append(
            {
                "from": item["rsID"],
                "to": item["expID"],
                "dashes": "true",
                "title": "NA",
                "color": {"color": "gray"},
            }
        )
        res["links"].append(
            {
                "from": item["rsID"],
                "to": item["outID_mrbase"],
                "arrows": "to",
                "color": {"color": "gray"},
            }
        )
        res["links"].append(
            {
                "from": item["outID_mrbase"],
                "to": item["expID"],
                "arrows": "to",
                "title": item["rsID"] + ": coloc (pass); direction (fail)",
                "color": {"color": "red", "highlight": "red", "hover": "red"},
            }
        )
    elif (
        item["direction"] == "FALSE"
        and item["steiger_pvalue"] < PVALUE_THR_STEIGER
        and item["coloc_prob"] < COLOC_THR
    ):
        res["links"].append(
            {
                "from": item["rsID"],
                "to": item["expID"],
                "dashes": "true",
                "title": "NA",
                "color": {"color": "gray"},
            }
        )
        res["links"].append(
            {
                "from": item["rsID"],
                "to": item["outID_mrbase"],
                "arrows": "to",
                "color": {"color": "gray"},
            }
        )
        res["links"].append(
            {
                "from": item["outID_mrbase"],
                "to": item["expID"],
                "arrows": "to",
                "title": item["rsID"] + ": coloc (fail); direction (fail)",
                "color": {"color": "red", "highlight": "red", "hover": "red"},
            }
        )
    else:
        res["links"].append(
            {
                "from": item["rsID"],
                "to": item["expID"],
                "dashes": "true",
                "title": "NA",
                "color": {"color": "gray"},
            }
        )
        res["links"].append(
            {
                "from": item["rsID"],
                "to": item["outID_mrbase"],
                "dashes": "true",
                "title": "NA",
                "color": {"color": "gray"},
            }
        )
        res["links"].append(
            {
                "from": item["outID_mrbase"],
                "to": item["expID"],
                "dashes": "true",
                "title": item["rsID"] + ": coloc (none); direction (none)",
                "color": {"color": "gray"},
            }
        )
    return res, nodes
