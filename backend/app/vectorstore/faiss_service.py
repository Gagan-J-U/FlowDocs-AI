import os
import pickle

import faiss
import numpy as np


VECTOR_STORAGE_DIR = "vector_storage"

_index_cache = {}


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

    cache_key = (
        str(workspace_id),
        str(subject_id)
    )

    if cache_key in _index_cache:

        return _index_cache[cache_key]

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

    _index_cache[cache_key] = (
        index,
        chunk_ids
    )

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

    _index_cache[
        (
            str(workspace_id),
            str(subject_id)
        )
    ] = (
        index,
        chunk_ids
    )


# ==========================================
# SAVE BM25 CORPUS
# ==========================================

def save_bm25_corpus(

    workspace_id: str,

    subject_id: str,

    chunks: list
):

    subject_dir = get_subject_directory(

        workspace_id,
        subject_id
    )

    os.makedirs(
        subject_dir,
        exist_ok=True
    )

    corpus_path = os.path.join(
        subject_dir,
        "bm25_corpus.pkl"
    )

    index_path = os.path.join(
        subject_dir,
        "bm25_index.pkl"
    )

    corpus_by_id = {}

    if os.path.exists(corpus_path):

        with open(corpus_path, "rb") as file:

            existing_corpus = pickle.load(file)

        corpus_by_id = {
            chunk["chunk_id"]: chunk
            for chunk in existing_corpus
        }

    for chunk in chunks:

        corpus_by_id[chunk["chunk_id"]] = {

            "chunk_id": chunk["chunk_id"],

            "text": chunk["text"]
        }

    with open(corpus_path, "wb") as file:

        pickle.dump(
            list(corpus_by_id.values()),
            file
        )

    if os.path.exists(index_path):

        os.remove(index_path)


# ==========================================
# LOAD BM25 CORPUS
# ==========================================

def load_bm25_corpus(

    workspace_id: str,

    subject_id: str
):

    subject_dir = get_subject_directory(

        workspace_id,
        subject_id
    )

    corpus_path = os.path.join(
        subject_dir,
        "bm25_corpus.pkl"
    )

    if not os.path.exists(corpus_path):

        return []

    with open(corpus_path, "rb") as file:

        corpus = pickle.load(file)

    return corpus


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
