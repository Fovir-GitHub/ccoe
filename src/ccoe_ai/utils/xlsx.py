import pandas as pd


def read_xlsx(path: str) -> pd.DataFrame:
    """
    Read an Excel data file into a pandas `DataFrame`.

    This function reads the Excel file at the given path, and
    - Drops unnamed columns
    - Strips leading and trailing whitespaces from column headers

    Parameters
    ----------
    path : str
        Path to the Excel file.

    Returns
    -------
    pandas.DataFrame
        The Excel data with cleaned column names.
    """

    df = pd.read_excel(path)
    df.columns = df.columns.str.strip()

    return df
