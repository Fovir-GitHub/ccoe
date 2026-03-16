from pydantic_settings import BaseSettings, SettingsConfigDict
from .embedding import EmbeddingSettings


class Settings(BaseSettings):
    embedding: EmbeddingSettings = EmbeddingSettings()

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP_",
        env_nested_delimiter="__",
    )


settings = Settings()
