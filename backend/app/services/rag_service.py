from app.services.embedding_service import get_embeddings
from app.db.faiss_manager import search
from app.services.llm_service import generate_response
from sentence_transformers import CrossEncoder

cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def generate_rag_response(subject_id: str, query: str, history: list[str]):

    # 🔹 Step 1: Embed query
    query_embedding = get_embeddings([query])[0]

    # 🔹 Step 2: Retrieve more (IMPORTANT)
    results = search(subject_id, query_embedding, top_k=20)

    # 🔹 Step 3: Handle empty retrieval
    if not results:
        return {
            "answer": "I could not find relevant information in the documents.",
            "sources": []
        }

    # 🔹 Step 4: Re-rank
    reranked = rerank(query, results)

    # 🔹 Step 5: Filter noise
    filtered = filter_chunks(reranked)

    if not filtered:
        filtered = reranked[:5]  # fallback

    # 🔹 Step 6: Select top chunks
    final_chunks = filtered[:5]

    # 🔹 Step 7: Build context
    context = build_context(final_chunks)

    # 🔥 STRONG SYSTEM PROMPT
    prompt = f"""
    You are an AI assistant that answers using ONLY the provided context.

    RULES:
    - Use the context to understand and explain, not copy sentences
    - Summarize in your own words
    - Keep answers short and clear
    - If answer is not in context, say:
    "I could not find the answer in the provided documents."
    - Add sources at the end of each point
    - Do NOT hallucinate

    Format:
    - Use bullet points
    - Rewrite in simple language

    Context:
    {context}

    Question:
    {query}

    Answer:
    """

    # 🔹 Step 8: Generate response
    response = generate_response(prompt)

    # 🔹 Step 9: Attach sources
    sources = [
        {
            "document": c["document_name"],
            "page": c["page"]
        }
        for c in final_chunks
    ]

    return {
        "answer": response,
        "sources": sources
    }

def rerank(query, chunks):
    if not chunks:
        return []

    pairs = [[query, c["text"]] for c in chunks]
    scores = cross_encoder.predict(pairs)

    for i, score in enumerate(scores):
        chunks[i]["rerank_score"] = float(score)

    chunks.sort(key=lambda x: x["rerank_score"], reverse=True)
    return chunks


def filter_chunks(chunks, threshold=0.3):
    return [c for c in chunks if c.get("rerank_score", 0) >= threshold]


def build_context(chunks):
    context = ""

    for i, chunk in enumerate(chunks):
        context += f"""
        [Source {i+1}]
        Document: {chunk['document_name']}
        Page: {chunk['page']}
        Content:
        {chunk['text']}

        """
    return context