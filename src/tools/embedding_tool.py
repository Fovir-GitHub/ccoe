from langchain.tools import tool

from src.services.build_embeddings import build_embeddings

@tool
def generate_embedding_from_excel(input_path: str, output_path: str):
    """
    Generate embeddings from an Excel file.

    :param input_path: Path to input Excel file
    :param output_path: Path to save embedding file
    :return: The path to the saved embedding file.
    """
    return build_embeddings(input_path, output_path)