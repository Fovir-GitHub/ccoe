MODEL_CONFIG = {
    "embedding_model": {
        "backend": "huggingface",  # alternate ["huggingface", "ollama"]
        "model_name": "maidalun1020/bce-embedding-base_v1",
        "dtype": "float16",
        "device": "auto",
        "trust_remote_code": True
    }
}