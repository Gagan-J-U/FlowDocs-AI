from sentence_transformers import (
    SentenceTransformer
)

import numpy as np


# ==========================================
# LOAD MODEL
# ==========================================

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ==========================================
# GENERATE SINGLE EMBEDDING
# ==========================================

def generate_embedding(text: str):

    embedding = embedding_model.encode(
        text,
        normalize_embeddings=True
    )

    return embedding.astype(
        np.float32
    )


# ==========================================
# GENERATE MULTIPLE EMBEDDINGS
# ==========================================

def generate_embeddings(texts):

    embeddings = embedding_model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    return np.array(
        embeddings,
        dtype=np.float32
    )