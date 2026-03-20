from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from src.ccoe_ai.config import settings
from src.ccoe_ai.tools import TOOL_LIST
import structlog

logger = structlog.get_logger(__name__)


def init_llm() -> BaseChatModel:
    logger.info("init_llm_called")

    llm: BaseChatModel
    temperature = settings.agent.temperature
    provider = settings.agent.provider
    model = settings.agent.model

    logger.info(
        "loading_llm",
        provider=provider,
        model=model,
    )

    match (provider):
        case "ollama":
            llm = ChatOllama(
                model=model,
                temperature=temperature,
                base_url=settings.agent.endpoint,
            )
        case "openai":
            llm = ChatOpenAI(
                model=model,
                temperature=temperature,
                base_url=settings.agent.endpoint,
                api_key=SecretStr(settings.agent.api_key),
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
            "You are an expert Deduplication Auditor. Analyze the data sample and provide an audit summary. "
            "Do NOT output the full dataset as it is already saved to a file.",
        ),
        (
            "human",
            "Here is a sample of the deduplicated records:\n{data}\n\n"
            "Please provide an audit report including the top 3 potential duplicate sets identified.",
        ),
    ]
)
