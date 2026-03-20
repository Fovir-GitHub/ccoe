import structlog
import pandas as pd
from langchain_core.messages import HumanMessage
from src.ccoe_ai.tools.embedding_tool import generate_embedding_from_excel
from .llm import llm_with_tools

logger = structlog.get_logger(__name__)


def invoke_embedding_agent(data: dict) -> dict:
    normalized_path = data["normalized_path"]
    output_path = data["output_path"]
    logger.info(
        "invoke_embedding_agent",
        normalized_path=normalized_path,
        output_path=output_path,
    )

    # Natural-language task handed to the agent
    task_message = HumanMessage(
        content=(
            f"Generate embeddings for the Excel file at {normalized_path} and save the result to {output_path}."
        )
    )

    # LLM reasons about the task and emits tool_calls
    ai_message = llm_with_tools.invoke([task_message])
    logger.debug(
        "llm_response_received",
        tool_calls=getattr(ai_message, "tool_calls", None),
        content=getattr(ai_message, "content", None),
    )

    parquet_path = output_path  # fallback

    # execute the tool calls emitted by the LLM agent
    for tool_call in ai_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        logger.debug(
            "tool_call_received",
            tool_name=tool_name,
            tool_args=tool_args,
        )

        if tool_name == generate_embedding_from_excel.name:
            logger.info(
                "calling_embedding_tool",
                tool_name=tool_name,
            )
            result = generate_embedding_from_excel.invoke(tool_args)
            parquet_path = result
    return {"parquet_path": parquet_path}


def load_embeddings(data: dict) -> dict:
    logger.debug("load_embedding_start")
    df = pd.read_parquet(data["parquet_path"])
    sample = df.head(5).drop(
        columns=["embedding"], errors="ignore"
    )  # this row for testing!!! If can run, just deletee this row and modify sample as df
    result = {"data": sample.to_markdown()}
    logger.debug(
        "load_embedding_complete",
        result_keys=list(result.keys()),
    )
    return result
