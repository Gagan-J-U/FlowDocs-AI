from app.services.embedding_service import get_embeddings
from app.db.faiss_manager import search
from app.services.llm_service import generate_response


def generate_rag_response(subject_id: str, query: str, history: list[str]):    
    query_embedding = get_embeddings([query])

    results = search(subject_id, query_embedding, top_k=5)

    context = "\n\n".join([r["text"] for r in results])

    prompt = f"""
    You are an AI assistant.

    Use ONLY the context below to answer.

    Context:
    {context}

    Question:
    {query}

    Answer clearly:
    """

    response = generate_response(prompt)

    return response