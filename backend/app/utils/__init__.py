import json
from pathlib import Path
from typing import Optional, Union

import numpy as np
import requests

color_palette_file = Path(__file__).parent / "colorscheme.json"
rpkg_file = Path(__file__).parent / "rpkg-funcs.yml"

with open(color_palette_file, "r") as f:
    color_palette = json.load(f)

unittest_headers = {"client-type": "pytest", "ci": "true"}
api_request_headers = {"client-type": "webui", "ci": "false"}


def bin_rescale(x: np.array, n_bins, min=0.0, max=1.0):  # type: ignore
    """For a numeric x, convert them to their bins,
    then rescale them.
    """
    x1 = np.digitize(x, range(n_bins))
    rescaled = (np.max(x1) - np.min(x1)) * (x - np.min(x1)) / (
        max - min
    ) + np.min(x1)
    return rescaled


def hex_to_rgb(hex: str, alpha: Union[float, None] = None) -> str:
    """ "#B4FBBB" -> "rgb(180, 251, 187)" """
    hex = hex.lstrip("#")
    rr = int(hex[0:2], 16)
    gg = int(hex[2:4], 16)
    bb = int(hex[4:6], 16)
    if alpha:
        return f"rgba({rr}, {gg}, {bb}, {alpha})"
    else:
        return f"rgb({rr}, {gg}, {bb})"


def safe_none(x: Optional[str]) -> Optional[str]:
    """Convert str "None" to None."""
    if x == "None":
        return None
    else:
        return x


def overwrite_docker_url(
    url,
    pattern: str = "http://api_private:80",
    replacement: str = "http://api.epigraphdb.org",
):
    """When deployed inside docker-compose with api,
    the api url is passed as "api". This replace the "api" url with the
    real url.
    """
    return url.replace(pattern, replacement)


def batch_by_n(collection, batch_size):
    """Divide an iterable to sub chunks with size n.

    NOTE: this returns a generator
    """
    for i in range(0, len(collection), batch_size):
        yield collection[i : (i + batch_size)]


def ping_endpoint(url: str) -> bool:
    """Ping a GET endpoint that is expected to return a True."""
    try:
        r = requests.get(url, headers=api_request_headers)
        r.raise_for_status()
        res = r.json()
        assert res is True
    except:
        return False
    return True


def get_node_role(reference_node_is_source: bool) -> str:
    """Target in this case refers to the role of the reference node,
    if the reference node is a source, then the node is a target node.
    """
    if reference_node_is_source:
        return "target"
    else:
        return "source"


def format_triple(
    reference_meta_node: str,
    meta_node: str,
    meta_rel: str,
    reference_source_p: bool,
):
    template = "({reference_meta_node}){lhs_arrow}-[{meta_rel}]-{rhs_arrow}({meta_node})"
    if reference_source_p:
        lhs_arrow = ""
        rhs_arrow = ">"
    else:
        lhs_arrow = "<"
        rhs_arrow = ""
    return template.format(
        reference_meta_node=reference_meta_node,
        meta_node=meta_node,
        meta_rel=meta_rel,
        lhs_arrow=lhs_arrow,
        rhs_arrow=rhs_arrow,
    )
