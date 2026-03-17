import logging
import sys
from src.ccoe_ai.workflow import get_chain
from src.ccoe_ai.utils import init_logger


def main():
    init_logger()

    if len(sys.argv) < 2:
        logging.error("No path provided")
        sys.exit(1)

    excel_path = str(sys.argv[1])
    logging.info(f"get excel path: {excel_path}")
    chain = get_chain()
    result = chain.invoke(excel_path)
    print(result)


if __name__ == "__main__":
    main()
