import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def topk_similarity(query_embedding, embeddings, k=5):
    """
    Compute the top-k most similar embeddings to a query embedding using cosine similarity.

    :param query_embedding: The embedding vector of the query, where d is the embedding dimension.
    :param embeddings: A 2D array containing n embeddings to compare against the query.
    :param k: The number of top similar embeddings to return.

    :return: tuple (topk_idx, topk_sims)
        topk_idx: Indices of the top-k most similar embeddings in descending similarity order.
        topk_sims: Cosine similarity scores corresponding to the top-k indices.
    """
    sims = cosine_similarity([query_embedding], embeddings)[0]

    topk_idx = np.argsort(sims)[-k:][::-1]

    return topk_idx, sims[topk_idx]

