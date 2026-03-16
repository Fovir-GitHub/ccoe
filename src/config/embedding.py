from pydantic import BaseModel, field_validator
import torch


class EmbeddingSettings(BaseModel):
    backend: str = "huggingface"  # alternate ["huggingface", "ollama"]
    model_name: str = "maidalun1020/bce-embedding-base_v1"
    dtype: str = "float16"
    device: str = "auto"
    trust_remote_code: bool = True

    @field_validator("dtype", mode="after")
    def convert_dtype(cls, v):
        try:
            return getattr(torch, v)
        except AttributeError:
            raise ValueError(f"Invalid torch dtype: {v}")
