import os
import tempfile
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import HumanMessage

from src.normalization import normalization
from src.utils.xlsx_read import read_excel
from src.tools.embedding_tool import generate_embedding_from_excel

# get API key
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# paths to exceel (dummy data)
current_path = Path(__file__).resolve()
project_root = current_path.parent.parent
excel_path = project_root / "data" / "dummy.xlsx"

# set up llm with tool binding
llm = ChatOpenAI(model="gpt-4o", temperature=0)
llm_with_tools = llm.bind_tools([generate_embedding_from_excel])


# 1. Normalize
def normalize_and_stage(input_path: str) -> dict:
    df = read_excel(input_path)
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
        content=(f"Generate embeddings for the Excel file at {normalized_path} and save the result to {output_path}.")
    )

    # LLM reasons about the task and emits tool_calls
    ai_message = llm_with_tools.invoke([task_message])

    parquet_path = output_path  # fallback

#eexecute the tool calls emitted by the LLM agent
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
    sample = df.head(5).drop(columns=["embedding"], errors="ignore") # this row for testing!!! If can run, just deletee this row and modify sample as df
    return {"data": sample.to_markdown()}


# 4. design prompt
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a data deduplication expert.
Your task is to detect accounts that likely belong to the same person and combine them according to the embeeddings.
Return a CSV table.
""",
    ),
    ("human", "Here are database records:{data}Find duplicates."),
])

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