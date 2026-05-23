from sqlalchemy.orm import Session
from time import perf_counter
import os

from app.models.chunk import Chunk

from app.embeddings.embedding_service import (
    generate_embedding
)

from app.vectorstore.faiss_service import (
    search_index
)

from app.rag.bm25_cache import (
    bm25_cache
)


def retrieve_chunks(
    db: Session,
    workspace_id: str,
    subject_id: str,
    query: str,
    top_k: int = 5,
    use_reranker: bool = False,
    dense_top_k: int = 10,
    sparse_top_k: int = 10,
    rerank_top_n: int = 10
):

    timings_enabled = (
        os.getenv("RAG_TIMING", "0") == "1"
    )

    timings = {}

    stage_start = perf_counter()

    # ==========================================
    # Generate Query Embedding
    # ==========================================

    query_embedding = generate_embedding(
        query
    )

    timings["embedding"] = perf_counter() - stage_start

    # ==========================================
    # Dense Retrieval (FAISS)
    # ==========================================

    stage_start = perf_counter()

    dense_results = search_index(

        workspace_id=workspace_id,

        subject_id=subject_id,

        query_embedding=query_embedding,

        top_k=dense_top_k
    )

    timings["faiss"] = perf_counter() - stage_start

    if not dense_results:

        return []

    # ==========================================
    # Dense Chunk IDs + Scores
    # ==========================================

    dense_chunk_ids = [

        result["chunk_id"]

        for result in dense_results
    ]

    dense_score_map = {

        result["chunk_id"]: result["score"]

        for result in dense_results
    }

    dense_rank_map = {
        result["chunk_id"]: rank
        for rank, result in enumerate(dense_results, start=1)
    }

    # ==========================================
    # Sparse Retrieval (BM25)
    # ==========================================

    stage_start = perf_counter()

    bm25_index = bm25_cache.get_index(

        workspace_id=workspace_id,

        subject_id=subject_id
    )

    sparse_results = bm25_index.search(

        query=query,

        top_k=sparse_top_k
    )

    timings["bm25"] = perf_counter() - stage_start

    # ==========================================
    # Sparse Chunk IDs + Scores
    # ==========================================

    sparse_chunk_ids = [

        result["chunk_id"]

        for result in sparse_results
    ]

    bm25_score_map = {

        result["chunk_id"]: result["bm25_score"]

        for result in sparse_results
    }

    sparse_rank_map = {
        result["chunk_id"]: rank
        for rank, result in enumerate(sparse_results, start=1)
    }

    # ==========================================
    # Merge Chunk IDs
    # ==========================================

    merged_chunk_ids = list(dict.fromkeys(
        dense_chunk_ids + sparse_chunk_ids
    ))

    # ==========================================
    # Bulk Load ALL Chunks
    # ==========================================

    stage_start = perf_counter()

    chunks = (

        db.query(Chunk)

        .filter(
            Chunk.id.in_(merged_chunk_ids)
        )

        .all()
    )

    timings["db"] = perf_counter() - stage_start

    # ==========================================
    # Chunk Lookup Map
    # ==========================================

    chunk_map = {

        chunk.id: chunk

        for chunk in chunks
    }

    # ==========================================
    # Build Hybrid Payloads
    # ==========================================

    stage_start = perf_counter()

    hybrid_results = []

    for chunk_id in merged_chunk_ids:

        chunk = chunk_map.get(chunk_id)

        if not chunk:
            continue

        similarity_score = float(
            dense_score_map.get(
                chunk_id,
                0.0
            )
        )

        bm25_score = float(
            bm25_score_map.get(
                chunk_id,
                0.0
            )
        )

        hybrid_score = (
            1.0 / (60 + dense_rank_map[chunk_id])
            if chunk_id in dense_rank_map
            else 0.0
        ) + (
            1.0 / (60 + sparse_rank_map[chunk_id])
            if chunk_id in sparse_rank_map
            else 0.0
        )

        hybrid_results.append({

            "chunk_id": chunk.id,

            "text": chunk.text,

            "similarity_score": similarity_score,

            "bm25_score": bm25_score,

            "hybrid_score": hybrid_score,

            "document_id": chunk.document_id,

            "section_title": chunk.section_title,

            "parent_section": chunk.parent_section,

            "hierarchy_level": chunk.hierarchy_level,

            "start_page": chunk.start_page,

            "end_page": chunk.end_page
        })

    hybrid_results.sort(
        key=lambda result: result["hybrid_score"],
        reverse=True
    )

    timings["merge"] = perf_counter() - stage_start

    if not use_reranker:

        if timings_enabled:

            print(f"RAG timings: {timings}")

        return hybrid_results[:top_k]

    # Import lazily because loading the cross-encoder is expensive.
    stage_start = perf_counter()

    from app.rag.reranker import reranker

    reranked_chunks = reranker.rerank(
        query=query,
        chunks=hybrid_results[:rerank_top_n],
        top_k=top_k
    )

    timings["rerank"] = perf_counter() - stage_start

    if timings_enabled:

        print(f"RAG timings1: {timings}")

    return reranked_chunks
