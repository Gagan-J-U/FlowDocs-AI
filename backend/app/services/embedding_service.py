from sentence_transformers import SentenceTransformer
import numpy as np

# ==============================
# LOAD MODEL (ONLY ONCE)
# ==============================

model = SentenceTransformer("all-MiniLM-L6-v2")


# ==============================
# EMBEDDING FUNCTION
# ==============================

def get_embeddings(texts):
    """
    Generate embeddings for a list of texts.

    Always returns:
    numpy array of shape (n, dim)
    """

    # 🔴 Safety: handle single string input
    if isinstance(texts, str):
        texts = [texts]

    # 🔴 Safety: empty input
    if not texts:
        return np.array([])

    # 🔥 Generate embeddings
    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True  # ✅ IMPORTANT (better similarity)
    )

    # 🔴 Safety: ensure 2D shape
    if len(embeddings.shape) == 1:
        embeddings = np.expand_dims(embeddings, axis=0)

    return embeddings