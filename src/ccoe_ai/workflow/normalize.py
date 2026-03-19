import structlog
from src.ccoe_ai.normalization import normalization
from src.ccoe_ai.utils import read_xlsx
import tempfile

logger = structlog.get_logger(__name__)


def normalize(path: str) -> dict:
    logger.debug(
        "normalize_start",
        input_path=path,
    )

    df = read_xlsx(path)
    df = df.drop(columns=["NO", "No", "Reg Date", "Exception"], errors="ignore")
    df = normalization(df)

    # store data temporarily so the @tool can read it by path
    tmp_xlsx = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False)
    tmp_parquet = tempfile.NamedTemporaryFile(suffix=".parquet", delete=False)

    logger.info(
        "normalize_temp_files_created",
        tmp_xlsx=tmp_xlsx.name,
        tmp_parquet=tmp_parquet.name,
    )

    tmp_xlsx.close()
    tmp_parquet.close()
    df.to_excel(tmp_xlsx.name, index=False)

    return {
        "normalized_path": tmp_xlsx.name,
        "output_path": tmp_parquet.name,
    }
