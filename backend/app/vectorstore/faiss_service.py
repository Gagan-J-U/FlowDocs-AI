import os
import pickle

import faiss
import numpy as np


VECTOR_STORAGE_DIR = "vector_storage"


# ==========================================
# GET SUBJECT STORAGE PATH
# ==========================================

def get_subject_directory(

    workspace_id: str,

    subject_id: str
):

    return os.path.join(

        VECTOR_STORAGE_DIR,

        workspace_id,

        subject_id
    )


# ==========================================
# CREATE EMPTY INDEX
# ==========================================

def create_empty_index(
    dimension: int
):

    return faiss.IndexFlatIP(
        dimension
    )


# ==========================================
# LOAD EXISTING INDEX
# ==========================================

def load_index_and_ids(

    workspace_id: str,

    subject_id: str
):

    subject_dir = get_subject_directory(

        workspace_id,
        subject_id
    )

    index_path = os.path.join(
        subject_dir,
        "index.faiss"
    )

    ids_path = os.path.join(
        subject_dir,
        "chunk_ids.pkl"
    )

    # No existing index
    if not os.path.exists(index_path):

        return None, []

    # Load FAISS index
    index = faiss.read_index(
        index_path
    )

    # Load chunk IDs
    with open(ids_path, "rb") as file:

        chunk_ids = pickle.load(file)

    return index, chunk_ids


# ==========================================
# SAVE INDEX + CHUNK IDS
# ==========================================

def save_index_and_ids(

    workspace_id: str,

    subject_id: str,

    index,

    chunk_ids
):

    subject_dir = get_subject_directory(

        workspace_id,
        subject_id
    )

    os.makedirs(
        subject_dir,
        exist_ok=True
    )

    # Save FAISS index
    faiss.write_index(

        index,

        os.path.join(
            subject_dir,
            "index.faiss"
        )
    )

    # Save chunk ID mapping
    with open(

        os.path.join(
            subject_dir,
            "chunk_ids.pkl"
        ),

        "wb"

    ) as file:

        pickle.dump(
            chunk_ids,
            file
        )


# ==========================================
# ADD NEW EMBEDDINGS
# ==========================================

def add_embeddings(

    workspace_id: str,

    subject_id: str,

    embeddings: np.ndarray,

    chunk_ids
):

    # Load existing index
    index, existing_chunk_ids = load_index_and_ids(

        workspace_id,
        subject_id
    )

    # First upload
    if index is None:

        dimension = embeddings.shape[1]

        index = create_empty_index(
            dimension
        )

    # Add embeddings
    index.add(embeddings)

    # Extend ID mapping
    existing_chunk_ids.extend(
        chunk_ids
    )

    # Save updated index
    save_index_and_ids(

        workspace_id,
        subject_id,

        index,

        existing_chunk_ids
    )


# ==========================================
# SEARCH
# ==========================================

def search_index(

    workspace_id: str,

    subject_id: str,

    query_embedding,

    top_k=5
):

    index, chunk_ids = load_index_and_ids(

        workspace_id,
        subject_id
    )

    if index is None:

        return []

    distances, indices = index.search(

        np.array(
            [query_embedding],
            dtype=np.float32
        ),

        top_k
    )

    results = []

    for score, idx in zip(

        distances[0],
        indices[0]
    ):

        if idx == -1:
            continue

        results.append({

            "score": float(score),

            "chunk_id": chunk_ids[idx]
        })

    return results