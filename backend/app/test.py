from services.embedding_service import get_embeddings
from db.faiss_manager import save_embeddings, search

texts = [
    "FastAPI is great",
    "Python is easy",
    "AI is future"
]

emb = get_embeddings(texts)

save_embeddings(1, emb, texts)

query = "What is good for backend?"
q_emb = get_embeddings([query])[0]

results = search(1, q_emb)

print(results)