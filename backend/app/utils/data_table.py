from typing import Dict, List, Optional, Union

import numpy as np
import pandas as pd

# global spec on rounding of numeric columns, e.g. effect size, standard error
ROUNDING = 4


def process_table_data(
    df: pd.DataFrame,
    cols_to_round: Optional[List[str]] = None,
    rounding: int = ROUNDING,
    to_dict: bool = True,
) -> Union[Dict, pd.DataFrame]:
    if cols_to_round is not None:
        rounding_configs = {col: rounding for col in cols_to_round}
        df = df.round(rounding_configs)
    df = df.replace({np.nan: None})
    if to_dict:
        df = df.to_dict(orient="records")
    return df
