from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from src.ccoe_ai.config import settings
from src.ccoe_ai.tools import TOOL_LIST
import logging


def init_llm() -> BaseChatModel:
    logging.info(f"init_llm called")

    llm: BaseChatModel
    temperature = settings.agent.temperature
    provider = settings.agent.provider
    model = settings.agent.model

    logging.info(f"loading LLM: provider {provider} model {model}")

    match (provider):
        case "ollama":
            llm = ChatOllama(
                model=model,
                temperature=temperature,
                base_url=settings.agent.endpoint,
            )
        case _:
            raise ValueError(f"Unsupported provider: {provider}")

    return llm


llm = init_llm()
llm_with_tools = llm.bind_tools(TOOL_LIST)

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
