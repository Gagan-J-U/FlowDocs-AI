from sentence_transformers import (
    SentenceTransformer
)

import numpy as np
import os


# ==========================================
# CONFIG
# ==========================================

MODEL_NAME = os.getenv(
    "EMBEDDING_MODEL",
    "BAAI/bge-base-en-v1.5"
)

LOCAL_FILES_ONLY = (
    os.getenv(
        "HF_LOCAL_FILES_ONLY",
        "1"
    ) != "0"
)

embedding_model = None


# ==========================================
# MODEL LOADER
# ==========================================

def get_embedding_model():

    global embedding_model

    if embedding_model is None:

        embedding_model = SentenceTransformer(

            MODEL_NAME,

            local_files_only=LOCAL_FILES_ONLY
        )

    return embedding_model


# ==========================================
# SINGLE EMBEDDING
# ==========================================

def generate_embedding(
    text: str
):

    model = get_embedding_model()

    embedding = model.encode(

        text,

        normalize_embeddings=True
    )

    return embedding.astype(
        np.float32
    )


# ==========================================
# BATCH EMBEDDINGS
# ==========================================

def generate_embeddings(
    texts
):

    model = get_embedding_model()

    embeddings = model.encode(

        texts,

        normalize_embeddings=True,

        batch_size=32,

        show_progress_bar=True
    )

    return np.array(

        embeddings,

        dtype=np.float32
    )