import io
import json
from typing import Any, Dict, List

import pandas as pd


def generate_df_descriptive_stats(df: pd.DataFrame):
    # df.info()
    buffer = io.StringIO()
    df.info(buf=buffer)
    info: str = buffer.getvalue()
    # df.describe()
    # NOTE: needs to re-serialise for the np int64 problem
    describe_json: str = (
        df.describe(include="all")
        .transpose()
        .reset_index()
        .rename(columns={"index": "variable"})
        .to_json(orient="records")
    )
    describe: List[Dict[str, Any]] = json.loads(describe_json)
    # combine
    res = {"info": info, "describe": describe}
    return res
