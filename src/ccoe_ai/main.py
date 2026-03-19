from src.ccoe_ai.utils import init_logger
from src.ccoe_ai.workflow import get_chain
import structlog
import sys

logger = structlog.get_logger(__name__)


def main():
    init_logger()

    if len(sys.argv) < 2:
        logger.error(
            "main_missing_argument",
            error="No path provided",
        )
        sys.exit(1)

    excel_path = str(sys.argv[1])
    logger.info(
        "main_start",
        excel_path=excel_path,
    )
    chain = get_chain()
    result = chain.invoke(excel_path)
    print(result)


if __name__ == "__main__":
    main()
