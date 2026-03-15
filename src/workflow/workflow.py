import os
import tempfile
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import HumanMessage

from src.normalization import normalization
from src.utils.xlsx_read import read_excel
from src.tools.embedding_tool import generate_embedding_from_excel

# get API key

load_dotenv()
#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HF_API_KEY = os.getenv("HF_API_KEY")

# paths to exceel (dummy data)
current_path = Path(__file__).resolve() # D:codeC/ccoe/src/workflow/workflow.py
project_root = current_path.parent.parent.parent # D:codeC/ccoe
excel_path = project_root / "data" / "dummy.xlsx" # D:codeC/ccoe/data/dummy.xlsx

# set up llm with tool binding
llm = ChatOllama(model="Qwen3.5:4b", temperature=0, base_url="http://localhost:11434")
llm_with_tools = llm.bind_tools([generate_embedding_from_excel])


# 1. Normalize
def normalize_and_stage(input_path: str) -> dict:
    df = read_excel(input_path)
    df.columns = df.columns.str.strip() # delete the space
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
Please process these records through the vectorization tool. Identify all potential duplicates and output the final deduplicated results in a CSV format.
"""
),
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