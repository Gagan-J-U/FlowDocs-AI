import faiss
import numpy as np
import os
import pickle

BASE_PATH = "faiss_indexes"


def get_index_path(subject_id):
    return f"{BASE_PATH}/subject_{subject_id}.index"


def get_meta_path(subject_id):
    return f"{BASE_PATH}/subject_{subject_id}.pkl"
  
def add_embeddings(subject_id, embeddings, metadata):
    index_path = get_index_path(subject_id)
    meta_path = get_meta_path(subject_id)

    embeddings = np.array(embeddings).astype("float32")

    if os.path.exists(index_path):
        index = faiss.read_index(index_path)

        with open(meta_path, "rb") as f:
            old_meta = pickle.load(f)

        index.add(embeddings)
        old_meta.extend(metadata)

        with open(meta_path, "wb") as f:
            pickle.dump(old_meta, f)

    else:
        dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(embeddings)

        with open(meta_path, "wb") as f:
            pickle.dump(metadata, f)

    faiss.write_index(index, index_path)

