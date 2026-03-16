from pydantic_settings import BaseSettings, SettingsConfigDict
from .embedding import EmbeddingSettings


class Settings(BaseSettings):
    """
    Application configuration.

    This Pydantic model loads configuration from environment variables and
    an optional `.env` file. Environment variables are expected to use the
    `APP_` prefix and nested structures are separated with `__`.

    Examples
    --------
    ````
    APP_EMBEDDING__API_KEY="sk-..."
    APP_EMBEDDING__MODEL_NAME="text-embedding-ada-002"
    ````
    """

    # Embedder configuration. Override defaults via APP_EMBEDDING__* environment variables.
    embedding: EmbeddingSettings = EmbeddingSettings()

    # Pydantic Settings configuration.
    # env_file: Path to .env file.
    # env_prefix: Prefix for all env vars (e.g., APP_EMBEDDING__API_KEY).
    # env_nested_delimiter: Delimiter for nested configs.
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP_",
        env_nested_delimiter="__",
    )


settings = Settings()
