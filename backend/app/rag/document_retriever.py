from sqlalchemy.orm import Session

from app.models.chunk import Chunk

from app.embeddings.embedding_service import (
    generate_embedding
)

from app.vectorstore.faiss_service import (
    search_index
)

from app.rag.reranker import (
    reranker
)


def retrieve_document_chunks(
    db: Session,
    workspace_id: str,
    subject_id: str,
    document_id: str,
    query: str,
    top_k: int = 5
):

    query_embedding = generate_embedding(
        query
    )

    search_results = search_index(
        workspace_id=workspace_id,
        subject_id=subject_id,
        query_embedding=query_embedding,
        top_k=50
    )

    chunk_ids = [
        result["chunk_id"]
        for result in search_results
    ]

    chunks = (
        db.query(Chunk)
        .filter(
            Chunk.id.in_(chunk_ids),
            Chunk.document_id == document_id
        )
        .all()
    )

    chunk_map = {
        chunk.id: chunk
        for chunk in chunks
    }

    retrieved_chunks = []

    for result in search_results:

        chunk = chunk_map.get(
            result["chunk_id"]
        )

        if not chunk:
            continue

        retrieved_chunks.append({

            "chunk_id": chunk.id,

            "text": chunk.text,

            "similarity_score": float(
                result["score"]
            ),

            "document_id": chunk.document_id,

            "section_title": chunk.section_title,

            "parent_section": chunk.parent_section,

            "hierarchy_level": chunk.hierarchy_level,

            "start_page": chunk.start_page,

            "end_page": chunk.end_page
        })

    return reranker.rerank(
        query=query,
        chunks=retrieved_chunks,
        top_k=top_k
    )