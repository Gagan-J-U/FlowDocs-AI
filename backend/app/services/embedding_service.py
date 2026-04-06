from sentence_transformers import SentenceTransformer

# Load once (global)
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embeddings(texts: list[str]):
    return model.encode(texts)