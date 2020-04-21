from textwrap import dedent
from typing import Dict, Optional

from app.funcs.curlify import to_curl
from app.settings import api_url
from app.utils import overwrite_docker_url


def render_query(
    r,
    empty_results: bool,
    url: Optional[str] = None,
    params: Optional[Dict] = None,
    limit: Optional[int] = 30,
) -> Dict[str, Optional[str]]:
    json_response = r.json()
    if limit is not None:
        json_response = truncate_response(json_response, limit=limit)
    api_snippet = None
    r_pkg_snippet = None
    if url is not None:
        api_snippet = render_api_snippet(url=url, params=params, method="GET")
        r_pkg_snippet = render_r_pkg_snippet(url=url, params=params)
    query = {
        "cypher": r.json()["metadata"]["query"],
        "curl": to_curl(r.request),
        "api_snippet": api_snippet,
        "r_pkg_snippet": r_pkg_snippet,
        "response_data": json_response,
        "empty_results": empty_results,
    }
    return query


# TODO: allow for POST request
def render_api_snippet(
    url: str, params: Optional[Dict], method: str = "GET"
) -> str:
    get_query_template = """
    import requests


    url = {url}
    params = {params}
    r = requests.get(url, params=params)
    r.raise_for_status()
    r.json()
    """
    query = dedent(get_query_template).format(
        url=overwrite_docker_url(url), params=str(params)
    )
    return query


def render_r_pkg_snippet(
    url: str, params: Optional[Dict], method: str = "GET"
) -> str:
    def format_route(url) -> str:
        res = url.replace(api_url, "")
        if res[0] != "/":
            res = "/" + res
        return res

    def format_arg_value(value) -> str:
        if type(value) is str:
            return f'"{value}"'
        elif type(value) is bool:
            return str(value).upper()
        else:
            return str(value)

    def format_params(params) -> str:
        res = ",".join(
            [
                f"{key}={format_arg_value(value)}"
                for key, value in params.items()
            ]
        )
        return res

    get_query_template = """
    library("tidyverse")
    library("epigraphdb")

    res = query_epigraphdb(
      route=\"{route}\",
      params=list({params}),
      mode="table"
    )
    res
    """
    query = dedent(get_query_template).format(
        route=format_route(url), params=format_params(params)
    )
    return query


def truncate_response(response, limit):
    new_response = {
        "query": response["metadata"]["query"],
        "results": response["results"][:limit],
    }
    return new_response
