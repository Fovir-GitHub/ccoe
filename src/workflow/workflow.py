import os
import tempfile
import pandas as pd
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import HumanMessage

from src.normalization import normalization
from src.utils import read_xlsx
from src.tools.embedding_tool import generate_embedding_from_excel

# get API key

load_dotenv()
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# paths to exceel (dummy data)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
excel_path = os.path.join(directory, "data/dummy.xlsx")


# set up llm with tool binding
llm = ChatOllama(model="Qwen3.5:4b", temperature=0, base_url="http://localhost:11434")
llm_with_tools = llm.bind_tools([generate_embedding_from_excel])


# 1. Normalize
def normalize_and_stage(input_path: str) -> dict:
    df = read_xlsx(input_path)
    df = df.drop(
        columns=["NO", "No", "Reg Date", "Exception"]
    )  # drop the columns that are not needed for deduplication
    df = normalization(df)

    # store data temporarily so the @tool can read it by path
    tmp_xlsx = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False)
    tmp_parquet = tempfile.NamedTemporaryFile(suffix=".parquet", delete=False)
    tmp_xlsx.close()
    tmp_parquet.close()
    df.to_excel(tmp_xlsx.name, index=False)

    return {
        "normalized_path": tmp_xlsx.name,
        "output_path": tmp_parquet.name,
    }


# 2. llm tries to call the tool; we execute the tool call
def invoke_embedding_agent(data: dict) -> dict:
    normalized_path = data["normalized_path"]
    output_path = data["output_path"]
    # Natural-language task handed to the agent
    task_message = HumanMessage(
        content=(
            f"Generate embeddings for the Excel file at {normalized_path} and save the result to {output_path}."
        )
    )

    # LLM reasons about the task and emits tool_calls
    ai_message = llm_with_tools.invoke([task_message])

    parquet_path = output_path  # fallback

    # eexecute the tool calls emitted by the LLM agent
    for tool_call in ai_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        if tool_name == generate_embedding_from_excel.name:
            result = generate_embedding_from_excel.invoke(tool_args)
            parquet_path = result
    return {"parquet_path": parquet_path}


# 3. load embeddings
def load_embeddings(data: dict) -> dict:
    df = pd.read_parquet(data["parquet_path"])
    sample = df.head(5).drop(
        columns=["embedding"], errors="ignore"
    )  # this row for testing!!! If can run, just deletee this row and modify sample as df
    return {"data": sample.to_markdown()}


# 4. design prompt
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
        You are an expert Deduplication Engine. Your goal is to identify redundant records within a dataset that likely belong to the same individual.
        ### OPERATIONAL PIPELINE:
        - 1. Vector Representation: Utilize the provided 'generate_embedding_from_excel' tool to generate embeddings for the normalized fields.
        - 2. Similarity Analysis: Calculate the Cosine Similarity between record embeddings.
        - 3. Decision Logic: Rows with high similarity scores across multiple attributes should be flagged as duplicates.
        """,
        ),
        (
            "human",
            """
        The following database records have been normalized from an Excel file:{data}
        Please process these records through the vectorization tool.
        According to the top k values returned by the embedding tool, eliminate the top 3 information that are most likely to be duplicates.
        Output the final deduplicated results in a CSV format.
        """,
        ),
    ]
)

output_parser = StrOutputParser()

chain = (
    RunnableLambda(normalize_and_stage)
    | RunnableLambda(invoke_embedding_agent)
    | RunnableLambda(load_embeddings)
    | prompt
    | llm
    | output_parser
)


result = chain.invoke(str(excel_path))
print(result)
