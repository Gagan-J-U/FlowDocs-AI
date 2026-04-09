import faiss
import numpy as np
import os
import pickle

BASE_PATH = "faiss_indexes"

# ✅ Ensure folder exists
os.makedirs(BASE_PATH, exist_ok=True)


# ==============================
# PATH HELPERS
# ==============================

def get_index_path(subject_id):
    return f"{BASE_PATH}/subject_{subject_id}.index"


def get_meta_path(subject_id):
    return f"{BASE_PATH}/subject_{subject_id}.pkl"


# ==============================
# ADD EMBEDDINGS
# ==============================

def add_embeddings(subject_id, embeddings, metadata):
    index_path = get_index_path(subject_id)
    meta_path = get_meta_path(subject_id)

    # 🔥 Convert to numpy
    embeddings = np.array(embeddings).astype("float32")

    # 🔴 FIX 1: Ensure 2D shape
    if len(embeddings.shape) == 1:
        embeddings = np.expand_dims(embeddings, axis=0)

    # 🔴 FIX 2: Empty check
    if embeddings.shape[0] == 0:
        print("❌ No embeddings to add")
        return

    # 🔴 FIX 3: Metadata length mismatch
    if len(metadata) != embeddings.shape[0]:
        print("❌ Metadata and embeddings count mismatch")
        return

    # ==============================
    # EXISTING INDEX
    # ==============================

    if os.path.exists(index_path):
        index = faiss.read_index(index_path)

        with open(meta_path, "rb") as f:
            old_meta = pickle.load(f)

        # 🔴 FIX 4: Dimension mismatch check
        if index.d != embeddings.shape[1]:
            print("❌ Embedding dimension mismatch")
            return

        index.add(embeddings)
        old_meta.extend(metadata)

        with open(meta_path, "wb") as f:
            pickle.dump(old_meta, f)

    # ==============================
    # NEW INDEX
    # ==============================

    else:
        dim = embeddings.shape[1]

        if dim == 0:
            print("❌ Invalid embedding dimension")
            return

        index = faiss.IndexFlatL2(dim)
        index.add(embeddings)

        with open(meta_path, "wb") as f:
            pickle.dump(metadata, f)

    # 🔹 Save index
    faiss.write_index(index, index_path)

    print(f"✅ Added {embeddings.shape[0]} embeddings to subject {subject_id}")


# ==============================
# SEARCH
# ==============================

def search(subject_id, query_embedding, top_k=20):
    index_path = get_index_path(subject_id)
    meta_path = get_meta_path(subject_id)

    # 🔴 Safety check
    if not os.path.exists(index_path) or not os.path.exists(meta_path):
        print("⚠️ No FAISS index found for subject")
        return []

    index = faiss.read_index(index_path)

    with open(meta_path, "rb") as f:
        metadata = pickle.load(f)

    # 🔥 Convert query embedding
    query_vector = np.array(query_embedding).astype("float32")

    # 🔴 FIX: Ensure correct shape
    if len(query_vector.shape) == 1:
        query_vector = np.expand_dims(query_vector, axis=0)

    # 🔴 Safety: dimension match
    if query_vector.shape[1] != index.d:
        print("❌ Query embedding dimension mismatch")
        return []

    # 🔍 Search
    distances, indices = index.search(query_vector, top_k)

    results = []

    for i, idx in enumerate(indices[0]):
        if idx == -1 or idx >= len(metadata):
            continue

        chunk = metadata[idx]

        results.append({
            "text": chunk.get("text", ""),
            "document_name": chunk.get("document_name", "Unknown"),
            "page": chunk.get("page", None),
            "score": float(distances[0][i])  # lower = better (L2)
        })

    return results