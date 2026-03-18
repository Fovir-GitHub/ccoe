import logging
from src.ccoe_ai.normalization import normalization
from src.ccoe_ai.utils import read_xlsx
import tempfile


def normalize(path: str) -> dict:
    logging.debug("normalize begin")

    df = read_xlsx(path)
    df = df.drop(columns=["NO", "No", "Reg Date", "Exception"], errors="ignore")
    df = normalization(df)

    # store data temporarily so the @tool can read it by path
    tmp_xlsx = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False)
    tmp_parquet = tempfile.NamedTemporaryFile(suffix=".parquet", delete=False)

    logging.info(f"normalize: tmp_xlsx {tmp_xlsx} tmp_parquet {tmp_parquet}")

    tmp_xlsx.close()
    tmp_parquet.close()
    df.to_excel(tmp_xlsx.name, index=False)

    return {
        "normalized_path": tmp_xlsx.name,
        "output_path": tmp_parquet.name,
    }
