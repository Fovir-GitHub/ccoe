import logging
import torch
from transformers import AutoTokenizer, AutoModel
from typing import List
from tqdm import tqdm
from src.config import settings


class EmbeddingGenerator:
    """
    A class to generate text embeddings using different backends.

    Attributes:
        config (dict): Model configuration dictionary.
        backend (str): Model backend, e.g., "huggingface" or "ollama".
        model_name (str): Name of the model to load.
        dtype (torch.dtype): Data type for model weights.
        device_map (str): Device mapping for model loading.
        tokenizer (AutoTokenizer): Tokenizer instance (HuggingFace only).
        model (AutoModel): Model instance.
        device (torch.device): Device where the model resides.
    """

    def __init__(self):
        """
        Initialize the embedding generator.

        Parameters
        ----------
        config: Custom configuration dictionary.
                Defaults to MODEL_CONFIG["embedding_model"].
        """
        self.backend = settings.embedding.backend
        self.model_name = settings.embedding.model_name
        self.dtype = settings.embedding.dtype
        self.device_map = settings.embedding.device

        logging.info(
            f"initialize embedding generator: backend {self.backend} model_name {self.model_name} dtype {self.dtype} device_map {self.device_map}"
        )

        if self.backend == "huggingface":
            self._init_hf_model()
        elif self.backend == "ollama":
            self._init_ollama_model()
        else:
            logging.error(f"unsupported backend: {self.backend}")
            raise ValueError(f"[!] Unsupported backend: {self.backend}")

    def _init_hf_model(self):
        """
        Initialize HuggingFace tokenizer and model.

        Loads the tokenizer and model from the HuggingFace hub with specified
        dtype and device mapping, and sets the model to evaluation mode.
        """
        trust_remote_code = settings.embedding.trust_remote_code
        logging.info(
            f"initializing HuggingFace model: trust_remote_code {trust_remote_code}"
        )

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=trust_remote_code,
        )
        self.model = AutoModel.from_pretrained(
            self.model_name,
            trust_remote_code=trust_remote_code,
            torch_dtype=self.dtype,
            device_map=self.device_map,
        ).eval()
        self.device = next(self.model.parameters()).device

    def _init_ollama_model(self):
        """
        Initialize Ollama model backend for local inference.

        Loads the Ollama model from local path and sets device.
        """
        logging.info("initializing Ollama model...")
        try:
            import ollama
        except ImportError:
            raise ImportError("Please install Ollama SDK: pip install ollama")

        self.ollama = ollama
        self.device = "cpu"

    def generate_embeddings(self, texts: List[str], batch_size=16) -> List[List[float]]:
        """
        Generate embeddings locally using transformers

        :param texts: To generate a list of texts for vectors.
        :param batch_size: The batch size of the model is entered each time, with a default value of 16.
        :return: The list of embeddings (float) corresponding to each text.
        """

        logging.info(f"start generating embeddings: batch_size {batch_size}")
        embeddings = []

        for i in tqdm(range(0, len(texts), batch_size), desc="Generating embeddings"):
            batch = texts[i : i + batch_size]
            logging.debug(f"generate embeddings: times {i} batch {batch}")

            if self.backend == "huggingface":
                inputs = self.tokenizer(
                    batch, padding=True, truncation=True, return_tensors="pt"
                ).to(self.device)

                # run model without gradient computation
                with torch.no_grad():
                    outputs = self.model(**inputs)

                # mean pooling of last hidden states to get sentence embeddings
                batch_embeddings = outputs.last_hidden_state.mean(dim=1)
                embeddings.extend(batch_embeddings.cpu().tolist())
            elif self.backend == "ollama":
                if not hasattr(self, "ollama"):
                    raise RuntimeError(
                        "[!] Ollama not initialized. Call _init_ollama_model first."
                    )

                response = self.ollama.embed(
                    model=self.model_name, input=batch  # list[str]
                )

                batch_embeddings = response.get("embeddings", [])
                embeddings.extend(batch_embeddings)

        return embeddings
