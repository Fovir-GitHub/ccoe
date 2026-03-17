import logging
import pandas as pd
from langchain_core.messages import HumanMessage
from src.ccoe_ai.tools.embedding_tool import generate_embedding_from_excel
from .llm import llm_with_tools


def invoke_embedding_agent(data: dict) -> dict:
    normalized_path = data["normalized_path"]
    output_path = data["output_path"]
    logging.info(
        f"invoke embedding agent: normalized_path {normalized_path} output_path {output_path}"
    )

    # Natural-language task handed to the agent
    task_message = HumanMessage(
        content=(
            f"Generate embeddings for the Excel file at {normalized_path} and save the result to {output_path}."
        )
    )

    # LLM reasons about the task and emits tool_calls
    ai_message = llm_with_tools.invoke([task_message])
    logging.debug(f"ai_message.tool_calls: {ai_message.tool_calls}")
    logging.debug(f"ai_message content: {ai_message.content}")

    parquet_path = output_path  # fallback

    # execute the tool calls emitted by the LLM agent
    for tool_call in ai_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        logging.debug(f"tool_call: tool_name {tool_name} tool_args {tool_args}")

        if tool_name == generate_embedding_from_excel.name:
            logging.info("calling tool generate_embedding_from_excel")
            result = generate_embedding_from_excel.invoke(tool_args)
            parquet_path = result
    return {"parquet_path": parquet_path}


def load_embeddings(data: dict) -> dict:
    logging.debug("load embedding begin")
    df = pd.read_parquet(data["parquet_path"])
    sample = df.head(5).drop(
        columns=["embedding"], errors="ignore"
    )  # this row for testing!!! If can run, just deletee this row and modify sample as df
    result = {"data": sample.to_markdown()}
    logging.debug(f"load_embeddings result: {result}")
    return result
