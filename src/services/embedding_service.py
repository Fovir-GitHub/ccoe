import torch
from transformers import AutoTokenizer, AutoModel
from typing import List
from tqdm import tqdm

from src.services.text_builder import row_to_text
from src.utils.xlsx_read import read_excel

MODEL_NAME = "nvidia/llama-embed-nemotron-8b"

# Initialize tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True
)

model = AutoModel.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True,
    torch_dtype=torch.float16, # use half precision to reduce memory
    device_map="auto"
).eval()

device = next(model.parameters()).device # get model device

def generate_embeddings(texts: List[str], batch_size=16) -> List[List[float]]:
    """
    Generate embeddings locally using transformers

    :param texts To generate a list of texts for vectors.
    :param batch_size: The batch size of the model is entered each time, with a default value of 16.
    :return: The list of embeddings (float) corresponding to each text.
    """

    embeddings = []

    for i in tqdm(range(0, len(texts), batch_size), desc="Gnerating embeddings"):
        batch = texts[i:i + batch_size]

        inputs = tokenizer(
            batch,
            padding=True,
            truncation=True,
            return_tensors="pt"
        ).to(model.device)

        # run model without gradient computation
        with torch.no_grad():
            outputs = model(**inputs)

        # mean pooling of last hidden states to get sentence embeddings
        batch_embeddings = outputs.last_hidden_state.mean(dim=1)

        embeddings.extend(batch_embeddings.cpu().tolist())

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

    print(f"Saved embeddings to {output_path}")
    return str(output_path)