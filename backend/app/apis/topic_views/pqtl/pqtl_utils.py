from typing import Any, Dict, List, Optional

import requests

from app.funcs.cache import cache_func_call
from app.settings import api_url
from app.utils import api_request_headers

PQTL_URL = f"{api_url}/pqtl/"
PQTL_PLEIO_URL = f"{api_url}/pqtl/pleio/"
PQTL_LIST_URL = f"{api_url}/pqtl/list/"


def query_api_pqtl(
    query: str, rtype: str, pvalue: float, searchflag: str
) -> Any:
    """Queries the pQTL DB to receive the MR results and/or
    other supporting information
    """
    params: Dict[str, Any] = {
        "query": query,
        "rtype": rtype,
        "pvalue": pvalue,
        "searchflag": searchflag,
    }
    r = requests.get(PQTL_URL, params=params, headers=api_request_headers)
    r.raise_for_status()
    res = r.json()
    return res


def query_api_pqtl_list(search_flag: str) -> List[str]:
    """Returns the list of searchable proteins or traits"""
    params: Dict[str, Any] = {"flag": search_flag}
    r = requests.get(PQTL_LIST_URL, params=params, headers=api_request_headers)
    r.raise_for_status()
    data = r.json()["results"]
    if search_flag == "exposures":
        res = [item["expID"] for item in data]
    elif search_flag == "outcomes":
        res = [item["outID"] for item in data]
    return res


def query_api_pqtl_pleio(rsid: str, prflag: str) -> Any:
    """"""
    params = {"rsid": rsid, "prflag": prflag}
    r = requests.get(
        PQTL_PLEIO_URL, params=params, headers=api_request_headers
    )
    r.raise_for_status()
    data = r.json()
    return data


def query_api_pqtl_cached(
    query: str,
    rtype: str,
    pvalue: float,
    searchflag: str,
    overwrite: bool = False,
) -> Any:
    """cached version of query_api_pqtl"""
    params: Dict[str, Any] = {
        "query": query,
        "rtype": rtype,
        "pvalue": pvalue,
        "searchflag": searchflag,
    }
    res = cache_func_call(
        coll_name="pqtl",
        func=query_api_pqtl,
        params=params,
        overwrite=overwrite,
    )
    return res


def calc_api_flag_pleio(rsid: str, prflag: str) -> str:
    """Tests for pleiotropy;
    Returns either the number or list of associated proteins

    prflag: ["count", "proteins"]
    returns: either "1" or "protein1,\nprotein2"
    """
    params = {"rsid": rsid, "prflag": prflag}
    data = cache_func_call(
        coll_name="pqtl_pleio",
        func=query_api_pqtl_pleio,
        params=params,
        overwrite=False,
    )
    if prflag == "count":
        ptcount = str(data["results"])
    else:
        results = [item["expID"] for item in data["results"]]
        ptcount = ",\n".join(results)
    return ptcount


def num_to_round(v: Optional[float], dec: int) -> Optional[float]:
    """Presents the numerical values in a rounded decimal format"""
    if v is not None:
        return round(v, dec)
    else:
        return v


def calc_flag_hetero(q_pvalue: Optional[float]) -> str:
    """Calculate a flag for the heterogeneity test
    (consistency of the combined instruments)
    """
    if q_pvalue is not None:
        if q_pvalue > 0.05:
            consist = "Yes"
        else:
            consist = "No"
    else:
        consist = "NA"
    return consist
