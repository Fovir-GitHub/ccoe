import os
from typing import List

import requests
from dotenv import load_dotenv

from src.services.text_builder import row_to_text
from src.utils.xlsx_read import read_excel

load_dotenv()
HF_API_KEY = os.getenv("HF_API_KEY")

MODEL_NAME = "nvidia/llama-embed-nemotron-8b"
API_URL = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{MODEL_NAME}"

def generate_embeddings(texts: List[str], batch_size=16):
    """
    Call Hugging Face embedding API to generate embeddings

    :param batch_size: batch size for API calls, default is 16
    :param texts: list of strings to generate embeddings for
    :return: list of strings to generate embeddings for
    """
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    embeddings = []

    for i in range(0, len(texts), batch_size): # batch response
        batch = texts[i:i+batch_size]
        response = requests.post(API_URL, headers=headers, json={"inputs": batch})

        if response.status_code != 200:
            raise ValueError(f"[!] API call failed: {response.status_code}, {response.text}")

        batch_emb = response.json()
        embeddings.extend(emb[0] for emb in batch_emb) # flatten

    return embeddings

def build_embeddings(input_path: str, output_path: str) -> str:
    """
    Generate embeddings from an Excel (.xlsx) file and save them to a Parquet file.

    :param input_path: Path to the input Excel file (.xlsx)
    :param output_path: Path where the output Parquet file with embeddings will be saved
    :return: The path to the saved Parquet file
    """

    df = read_excel(input_path) # read data
    texts = df.apply(row_to_text, axis=1).tolist() # transfer to texts
    embeddings = generate_embeddings(texts) # generate embedding
    df["embedding"] = embeddings
    df.to_parquet(output_path, index=False) # save as parquet without index

    return output_path