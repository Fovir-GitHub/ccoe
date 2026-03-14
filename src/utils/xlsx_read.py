import pandas as pd

def read_excel(path: str) -> pd.DataFrame:
    df = pd.read_excel(path)

    if df.empty:
        raise ValueError("Excel file is empty")

    return df