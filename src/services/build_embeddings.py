from typing import Optional

from src.utils import read_xlsx
from src.services.text_builder import row_to_text
from src.services.embedding_service import EmbeddingGenerator
from src.services.similarity import topk_similarity


def build_embeddings(
    input_path: str,
    output_path: str,
    generator: Optional[EmbeddingGenerator] = None,
    topk: int = 0,
) -> str:
    """
    Generate embeddings from an Excel (.xlsx) file and save them to a Parquet file.

    :param input_path: Path to the input Excel file (.xlsx)
    :param output_path: Path where the output Parquet file with embeddings will be saved
    :param generator: Transfer texts list into embeddings
    :param topk: If >0, compute top-k similar texts for each row and save as 'topk_sim'
    :return: The path to the saved Parquet file
    """

    generator = generator or EmbeddingGenerator()
    df = read_xlsx(input_path)  # read data
    texts = df.apply(row_to_text, axis=1).tolist()  # transfer to texts
    embeddings = generator.generate_embeddings(texts)  # generate embedding
    df["embedding"] = embeddings

    if topk > 0:
        topk_results = []
        for i, emb in enumerate(embeddings):
            idxs, sims = topk_similarity(emb, embeddings, k=topk + 1)  # self rank 1
            idxs = idxs[idxs != i]
            sims = sims[idxs != i]
            topk_results.append(list(zip(idxs.tolist(), sims.tolist())))
        df["tok_sim"] = topk_results

    df.to_parquet(output_path, index=False)  # save as parquet without index

    print(f"Saved embeddings to {output_path}")
    return str(output_path)
