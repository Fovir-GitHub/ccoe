from src.ccoe_ai.utils import init_logger, writeable
from src.ccoe_ai.workflow import get_chain
import structlog
import sys

logger = structlog.get_logger(__name__)


def main():
    init_logger()

    if len(sys.argv) < 3:
        logger.error(
            "main_missing_argument",
            error="missing input path or output path",
        )
        sys.exit(1)

    excel_path = str(sys.argv[1])
    result_path = str(sys.argv[2])
    logger.info(
        "main_start",
        excel_path=excel_path,
        result_path=result_path,
    )

    if not writeable(result_path):
        logger.error(
            "result path is not writeable",
            result_path=result_path,
            info="Please check that the directory exists and has the correct permissions.",
        )
        sys.exit(1)

    chain = get_chain()
    result = chain.invoke(
        {
            "input_path": excel_path,
            "result_path": result_path,
        }
    )
    print(result)


if __name__ == "__main__":
    main()
