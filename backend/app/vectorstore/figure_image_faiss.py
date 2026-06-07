import os
import pickle

import faiss
import numpy as np


FIGURE_IMAGE_DIR = (
    "figure_vector_storage"
)

_index_cache = {}


def get_subject_directory(
    workspace_id,
    subject_id
):
    return os.path.join(
        FIGURE_IMAGE_DIR,
        workspace_id,
        subject_id
    )


def load_index_and_ids(
    workspace_id,
    subject_id
):

    cache_key = (
        workspace_id,
        subject_id
    )

    if cache_key in _index_cache:
        return _index_cache[
            cache_key
        ]

    subject_dir = get_subject_directory(
        workspace_id,
        subject_id
    )

    index_path = os.path.join(
        subject_dir,
        "image_index.faiss"
    )

    ids_path = os.path.join(
        subject_dir,
        "image_ids.pkl"
    )

    if not os.path.exists(index_path):
        return None, []

    index = faiss.read_index(
        index_path
    )

    with open(ids_path, "rb") as file:
        figure_ids = pickle.load(
            file
        )

    _index_cache[
        cache_key
    ] = (
        index,
        figure_ids
    )

    return (
        index,
        figure_ids
    )


def save_index_and_ids(
    workspace_id,
    subject_id,
    index,
    figure_ids
):

    subject_dir = get_subject_directory(
        workspace_id,
        subject_id
    )

    os.makedirs(
        subject_dir,
        exist_ok=True
    )

    index_path = os.path.join(
        subject_dir,
        "image_index.faiss"
    )

    ids_path = os.path.join(
        subject_dir,
        "image_ids.pkl"
    )

    faiss.write_index(
        index,
        index_path
    )

    with open(ids_path, "wb") as file:
        pickle.dump(
            figure_ids,
            file
        )

    _index_cache[
        (
            workspace_id,
            subject_id
        )
    ] = (
        index,
        figure_ids
    )


def add_image_embeddings(
    workspace_id,
    subject_id,
    embeddings,
    figure_ids
):

    index, existing_ids = (
        load_index_and_ids(
            workspace_id,
            subject_id
        )
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
        figure_ids
    )

    save_index_and_ids(
        workspace_id,
        subject_id,
        index,
        existing_ids
    )


def search_image_index(
    workspace_id,
    subject_id,
    query_embedding,
    top_k=10
):

    index, figure_ids = (
        load_index_and_ids(
            workspace_id,
            subject_id
        )
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

            "figure_id":
            figure_ids[idx],

            "score":
            float(score)
        })

    return results