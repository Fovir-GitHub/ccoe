from langchain_core.runnables import RunnableLambda, RunnableSerializable
from src.ccoe_ai.utils import init_logger
from .embedding import invoke_embedding_agent, load_embeddings
from .llm import llm, prompt
from .normalize import normalize
from langchain_core.output_parsers import StrOutputParser


def get_chain() -> RunnableSerializable:
    output_parser = StrOutputParser()
    chain = (
        RunnableLambda(normalize)
        | RunnableLambda(invoke_embedding_agent)
        | RunnableLambda(load_embeddings)
        | prompt
        | llm
        | output_parser
    )

    return chain
