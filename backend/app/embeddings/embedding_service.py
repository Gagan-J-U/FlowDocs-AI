from sentence_transformers import (
    SentenceTransformer
)

import numpy as np
import os


# ==========================================
# LOAD MODEL
# ==========================================

MODEL_NAME = "all-MiniLM-L6-v2"

LOCAL_FILES_ONLY = (
    os.getenv("HF_LOCAL_FILES_ONLY", "1") != "0"
)

embedding_model = None


def get_embedding_model():

    global embedding_model

    if embedding_model is None:

        embedding_model = SentenceTransformer(
            MODEL_NAME,
            local_files_only=LOCAL_FILES_ONLY
        )

    return embedding_model


# ==========================================
# GENERATE SINGLE EMBEDDING
# ==========================================

def generate_embedding(text: str):

    embedding = get_embedding_model().encode(
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

    embeddings = get_embedding_model().encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    return np.array(
        embeddings,
        dtype=np.float32
    )
