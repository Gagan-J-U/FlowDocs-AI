from sqlalchemy.orm import Session

from app.models.chunk import Chunk

from app.embeddings.embedding_service import (
    generate_embedding
)

from app.vectorstore.faiss_service import (
    search_index
)


# ==========================================
# RETRIEVE RELEVANT CHUNKS
# ==========================================

def retrieve_chunks(

    query: str,

    workspace_id: str,

    subject_id: str,

    db: Session,

    top_k: int = 5
):

    # ======================================
    # GENERATE QUERY EMBEDDING
    # ======================================

    query_embedding = generate_embedding(
        query
    )

    # ======================================
    # SEARCH FAISS
    # ======================================

    search_results = search_index(

        workspace_id=workspace_id,

        subject_id=subject_id,

        query_embedding=query_embedding,

        top_k=top_k
    )

    retrieved_chunks = []

    # ======================================
    # FETCH CHUNKS FROM POSTGRES
    # ======================================

    for result in search_results:

        chunk_id = result["chunk_id"]

        similarity_score = result["score"]

        chunk = db.query(Chunk).filter(
            Chunk.id == chunk_id
        ).first()

        if not chunk:
            continue

        retrieved_chunks.append({

            "score": similarity_score,

            "chunk_id": chunk.id,

            "text": chunk.text,

            "section_title": chunk.section_title,

            "parent_section": chunk.parent_section,

            "hierarchy_level": chunk.hierarchy_level,

            "start_page": chunk.start_page,

            "end_page": chunk.end_page,

            "document_id": chunk.document_id
        })

    return retrieved_chunks