import pandas as pd


def pd_datatable_fmt(df: pd.DataFrame) -> str:
    """Format dataframe an html snippet to be used in datatable.
    """
    return df.to_html(
        index=False, classes="display", border=0, table_id="data-table-dt"
    )
