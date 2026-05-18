from sqlalchemy.orm import Session

from app.ingestion.pdf_extractor import (
    extract_pdf_content
)

from app.ingestion.section_detector import (
    build_sections
)

from app.ingestion.chunker import (
    chunk_sections
)

from app.ingestion.chunk_filter import (
    filter_chunks
)

from app.services.chunk_storage_service import (
    store_chunks
)

from app.embeddings.embedding_service import (
    generate_embeddings
)

from app.vectorstore.faiss_service import (
    add_embeddings
)


# ==========================================
# INGEST DOCUMENT
# ==========================================

def ingest_document(

    document,

    workspace_id: str,

    subject_id: str,

    db: Session
):

    print("\n========== INGESTION STARTED ==========\n")

    # ======================================
    # EXTRACT PDF CONTENT
    # ======================================

    extraction_result = extract_pdf_content(

        pdf_path=document.file_path,

        image_output_dir=(
            f"uploads/images/{document.id}"
        )
    )

    print("PDF extraction completed.")

    # ======================================
    # BUILD SECTIONS
    # ======================================

    sections = build_sections(

        extracted_pages=extraction_result[
            "pages"
        ],

        toc=extraction_result[
            "toc"
        ]
    )

    print(
        f"Sections detected: "
        f"{len(sections)}"
    )

    # ======================================
    # CHUNK SECTIONS
    # ======================================

    chunks = chunk_sections(
        sections
    )

    print(
        f"Chunks created: "
        f"{len(chunks)}"
    )

    # ======================================
    # FILTER CHUNKS
    # ======================================

    chunks = filter_chunks(
        chunks
    )

    print(
        f"Chunks after filtering: "
        f"{len(chunks)}"
    )

    # ======================================
    # STORE CHUNKS IN POSTGRES
    # ======================================

    stored_chunks = store_chunks(

        chunks=chunks,

        document_id=document.id,

        db=db
    )

    print(
        f"Chunks stored in DB: "
        f"{len(stored_chunks)}"
    )

    # ======================================
    # GENERATE EMBEDDINGS
    # ======================================

    chunk_texts = [

        chunk.text

        for chunk in stored_chunks
    ]

    embeddings = generate_embeddings(
        chunk_texts
    )

    print("Embeddings generated.")

    # ======================================
    # STORE IN FAISS
    # ======================================

    chunk_ids = [

        chunk.id

        for chunk in stored_chunks
    ]

    add_embeddings(

        workspace_id=workspace_id,

        subject_id=subject_id,

        embeddings=embeddings,

        chunk_ids=chunk_ids
    )

    print("FAISS index updated.")

    print("\n========== INGESTION COMPLETE ==========\n")

    return {

        "sections": len(sections),

        "chunks": len(stored_chunks)
    }