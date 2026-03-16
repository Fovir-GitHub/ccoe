from typing import Optional
import numpy as np

from src.ccoe_ai.utils import read_xlsx
from src.ccoe_ai.services.text_builder import row_to_text
from src.ccoe_ai.services.embedding_service import EmbeddingGenerator
from src.ccoe_ai.services.similarity import filter_similar


def build_embeddings(
    input_path: str,
    output_path: str,
    generator: Optional[EmbeddingGenerator] = None,
    threshold: float = 0.92,
) -> str:
    """
    Generate embeddings from an Excel (.xlsx) file, remove highly similar rows,
    and save the result to a Parquet file.

    :param input_path: Path to the input Excel file (.xlsx)
    :param output_path: Path where the output Parquet file with embeddings will be saved
    :param generator: Transfer texts list into embeddings
    :param threshold: Cosine similarity threshold for filtering duplicates
    :return: The path to the saved Parquet file
    """
    generator = generator or EmbeddingGenerator()

    df = read_xlsx(input_path)
    texts = df.apply(row_to_text, axis=1).tolist()

    embeddings = generator.generate_embeddings(texts)
    embeddings = np.array(embeddings)
    df["embedding"] = embeddings.tolist()

    keep_idx = filter_similar(embeddings, threshold=threshold)
    df = df.iloc[keep_idx].reset_index(drop=True)
    print(f"Kept {len(df)} out of {len(texts)} rows after filtering by threshold {threshold}")

    df.to_parquet(output_path, index=False)
    print(f"Saved deduplicated embeddings to {output_path}")

    return str(output_path)