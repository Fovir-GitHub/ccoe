import pandas as pd
from .phone import normalize_phone
from .country import normalize_country


def normalization(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize a data frame.

    Parameters
    ----------
    df : pandas.DataFrame
        The input data frame.

    Returns
    -------
    pandas.DataFrame
        A normalized data frame.
    """

    # Normalize country codes.
    df["Country"] = df["Country"].apply(lambda c: normalize_country(str(c)))

    # Normalize phone numbers.
    df["Phone"] = df.apply(
        lambda row: normalize_phone(str(row["Phone"]), str(row["Country"])), axis=1
    )

    return df
