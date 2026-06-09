import os
import pickle

import faiss
import numpy as np


RESEARCH_VECTOR_DIR = (
    "research_vector_storage"
)

_index_cache = {}


# ==========================================
# LOAD INDEX
# ==========================================

def load_index_and_ids():

    cache_key = "research"

    if cache_key in _index_cache:

        return _index_cache[
            cache_key
        ]

    index_path = os.path.join(

        RESEARCH_VECTOR_DIR,

        "research_index.faiss"
    )

    ids_path = os.path.join(

        RESEARCH_VECTOR_DIR,

        "research_ids.pkl"
    )

    if not os.path.exists(
        index_path
    ):

        return None, []

    index = faiss.read_index(
        index_path
    )

    with open(
        ids_path,
        "rb"
    ) as file:

        profile_ids = pickle.load(
            file
        )

    _index_cache[
        cache_key
    ] = (
        index,
        profile_ids
    )

    return (
        index,
        profile_ids
    )


# ==========================================
# SAVE INDEX
# ==========================================

def save_index_and_ids(

    index,

    profile_ids
):

    os.makedirs(

        RESEARCH_VECTOR_DIR,

        exist_ok=True
    )

    index_path = os.path.join(

        RESEARCH_VECTOR_DIR,

        "research_index.faiss"
    )

    ids_path = os.path.join(

        RESEARCH_VECTOR_DIR,

        "research_ids.pkl"
    )

    faiss.write_index(
        index,
        index_path
    )

    with open(
        ids_path,
        "wb"
    ) as file:

        pickle.dump(
            profile_ids,
            file
        )

    _index_cache[
        "research"
    ] = (
        index,
        profile_ids
    )


# ==========================================
# ADD PROFILES
# ==========================================

def add_profile_embeddings(

    embeddings: np.ndarray,

    profile_ids: list
):

    index, existing_ids = (
        load_index_and_ids()
    )

    if index is None:

        dimension = (
            embeddings.shape[1]
        )

        index = faiss.IndexFlatIP(
            dimension
        )

    index.add(
        embeddings
    )

    existing_ids.extend(
        profile_ids
    )

    save_index_and_ids(

        index=index,

        profile_ids=existing_ids
    )


# ==========================================
# SEARCH
# ==========================================

def search_profiles(

    query_embedding,

    top_k=10
):

    index, profile_ids = (
        load_index_and_ids()
    )

    if index is None:

        return []

    scores, indices = index.search(

        np.array(
            [query_embedding],
            dtype=np.float32
        ),

        top_k
    )

    results = []

    for score, idx in zip(

        scores[0],

        indices[0]
    ):

        if idx == -1:

            continue

        results.append({

            "profile_id":
            profile_ids[idx],

            "score":
            float(score)
        })

    return results

  # ==========================================
  # REBUILD INDEX
  # ==========================================

def rebuild_profile_index(

    embeddings: np.ndarray,

    profile_ids: list
):

    if len(profile_ids) == 0:

        return

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(
        dimension
    )

    index.add(
        embeddings
    )

    save_index_and_ids(

        index=index,

        profile_ids=profile_ids
    )