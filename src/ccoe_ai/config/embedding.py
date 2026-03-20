from pydantic import BaseModel, field_validator
import torch


class EmbeddingSettings(BaseModel):
    """
    Pydantic model for configuring embedding provider.
    """

    backend: str = "huggingface"  # Optional: "huggingface", "ollama"
    model_name: str = "maidalun1020/bce-embedding-base_v1"  # Model name
    dtype: str = "float16"  # Torch dtype as string; will be converted to torch.dtype
    device: str = "auto"  # Compute device; "auto" selects CUDA if available
    trust_remote_code: bool = (
        True  # Allow loading of remote model code (dangerous if untrusted)
    )

    @field_validator("dtype", mode="after")
    def convert_dtype(cls, v):
        """
        Convert the dtype string to an actual torch dtype.
        Raises `ValueError` if the string is not a valid torch dtype.
        """
        try:
            return getattr(torch, v)
        except AttributeError:
            raise ValueError(f"Invalid torch dtype: {v}")
