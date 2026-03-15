from typing import Optional

from src.utils.xlsx_read import read_excel
from src.services.text_builder import row_to_text
from src.services.embedding_service import EmbeddingGenerator

def build_embeddings(input_path: str, output_path: str, generator: Optional[EmbeddingGenerator] = None) -> str:
    """
    Generate embeddings from an Excel (.xlsx) file and save them to a Parquet file.

    :param input_path: Path to the input Excel file (.xlsx)
    :param output_path: Path where the output Parquet file with embeddings will be saved
    :param generator: Transfer texts list into embeddings
    :return: The path to the saved Parquet file
    """

    generator = generator or EmbeddingGenerator()
    df = read_excel(input_path) # read data
    texts = df.apply(row_to_text, axis=1).tolist() # transfer to texts
    embeddings = generator.generate_embeddings(texts) # generate embedding
    df["embedding"] = embeddings
    df.to_parquet(output_path, index=False) # save as parquet without index

    print(f"Saved embeddings to {output_path}")
    return str(output_path)