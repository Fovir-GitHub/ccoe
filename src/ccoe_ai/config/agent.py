from pydantic import BaseModel


class AgentSettings(BaseModel):
    """
    Pydantic model for configuring agent model provider.
    """

    api_key: str = ""  # API key to access the model
    endpoint: str = "http://localhost:11434"  # Endpoint of API call
    model: str = "Qwen3.5:4b"  # Model name
    provider: str = "ollama"  # Optional: "ollama", "openai"
    temperature: int = 0
