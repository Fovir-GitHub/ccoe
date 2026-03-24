import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def filter_similar(embeddings, threshold=0.9):
    """
    Remove embeddings that are too similar to each other based on cosine similarity.

    :param embeddings: 2D array of shape (n, d), n embeddings of dimension d.
    :param threshold: Cosine similarity threshold above which embeddings are considered duplicates.

    :return: indices of embeddings to keep (unique ones)
    """
    n = embeddings.shape[0]
    keep_mask = np.ones(n, dtype=bool)

    # Compute full similarity matrix
    sims = cosine_similarity(embeddings)

    for i in range(n):
        if not keep_mask[i]:
            continue
        # Mask out self-comparison
        for j in range(i + 1, n):
            if sims[i, j] >= threshold:
                keep_mask[j] = False  # Mark duplicates as False

    return np.where(keep_mask)[0]
