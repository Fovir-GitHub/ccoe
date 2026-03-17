from pydantic import BaseModel


class AgentSettings(BaseModel):
    """
    Pydantic model for configuring agent model provider.
    """

    provider: str = "ollama"
    api_key: str = ""
    model: str = "Qwen3.5:4b"
    temperature: int = 0
    endpoint: str = "http://localhost:11434"
