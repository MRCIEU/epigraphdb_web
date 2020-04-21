import json
from pathlib import Path
from typing import Optional, Union

import numpy as np
import pandas as pd

color_palette_file = Path(__file__).parent / "colorscheme.json"

with open(color_palette_file, "r") as f:
    color_palette = json.load(f)

unittest_headers = {"client-type": "pytest"}


def bin_rescale(x: np.array, n_bins, min=0.0, max=1.0):
    """For a numeric x, convert them to their bins,
    then rescale them.
    """
    x1 = np.digitize(x, range(n_bins))
    rescaled = (np.max(x1) - np.min(x1)) * (x - np.min(x1)) / (
        max - min
    ) + np.min(x1)
    return rescaled


def hex_to_rgb(hex: str, alpha: Union[float, None] = None) -> str:
    """ "#B4FBBB" -> "rgb(180, 251, 187)"
    """
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
    pattern: str = "http://api",
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


def format_df_results(df: pd.DataFrame):
    """A general processor to convert a pandas dataframe
    to a format used in the frontend.
    """
    res = {
        "table_titles": [{"label": title} for title in df.columns],
        "table_data": df.to_dict(orient="records"),
    }
    return res


def format_df_results_general(df: pd.DataFrame):
    """A general processor to convert a pandas dataframe
    to a format used in the frontend.
    """
    res = {
        "table_titles": [
            {"label": title, "key": title, "sortable": True}
            for title in df.columns
        ],
        "table_data": df.to_dict(orient="records"),
    }
    return res
