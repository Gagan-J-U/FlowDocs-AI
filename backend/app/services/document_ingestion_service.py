import logging

from sqlalchemy.orm import Session

from app.core.database import (
    SessionLocal
)

from app.models.document import (
    Document
)

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
    add_embeddings,
    save_bm25_corpus
)

from app.rag.bm25_cache import (
    bm25_cache
)

from app.services.figure_service import (
    store_figures
)

from app.services.figure_caption_index_service import (
    index_figure_captions
)

from app.services.figure_image_index_service import (
    index_figure_images
)


def ingest_document(
    document,
    workspace_id: str,
    subject_id: str,
    db: Session
):

    print("\n========== INGESTION STARTED ==========\n")

    # ======================================
    # EXTRACT PDF
    # ======================================

    extraction_result = extract_pdf_content(
        pdf_path=document.file_path,
        image_output_dir=f"uploads/images/{document.id}"
    )

    print("PDF extraction completed.")

    # ======================================
    # STORE FIGURES
    # ======================================

    stored_figures = store_figures(
        document_id=document.id,
        extracted_images=extraction_result["images"],
        db=db
    )

    document.processing_status = "figures_stored"
    db.add(document)
    db.commit()
    db.refresh(document)

    print(
        f"Figures stored: "
        f"{len(stored_figures)}"
    )

    # ======================================
    # BUILD SECTIONS
    # ======================================
    try:
        sections = build_sections(
            extracted_pages=extraction_result["pages"],
            toc=extraction_result["toc"]
        )
        print(f"Sections detected: {len(sections)}")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.exception("Error building sections for document %s", document.id)
        document.processing_status = "error_sections"
        db.add(document)
        db.commit()
        raise

    # ======================================
    # CHUNK
    # ======================================
    try:
        chunks = chunk_sections(sections)
        print(f"Chunks created: {len(chunks)}")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.exception("Error chunking sections for document %s", document.id)
        document.processing_status = "error_chunking"
        db.add(document)
        db.commit()
        raise

    # ======================================
    # FILTER
    # ======================================
    try:
        chunks = filter_chunks(chunks)
        print(f"Chunks after filtering: {len(chunks)}")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.exception("Error filtering chunks for document %s", document.id)
        document.processing_status = "error_filter"
        db.add(document)
        db.commit()
        raise

    # ======================================
    # STORE CHUNKS
    # ======================================
    try:
        stored_chunks = store_chunks(
            chunks=chunks,
            document_id=document.id,
            db=db
        )
        document.processing_status = "chunks_stored"
        db.add(document)
        db.commit()
        db.refresh(document)
        print(f"Chunks stored in DB: {len(stored_chunks)}")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.exception("Error storing chunks for document %s", document.id)
        document.processing_status = "error_chunk_store"
        db.add(document)
        db.commit()
        raise

    # ======================================
    # TEXT EMBEDDINGS
    # ======================================
    try:
        chunk_texts = [chunk.text for chunk in stored_chunks]
        embeddings = generate_embeddings(chunk_texts)
        document.processing_status = "text_embeddings_generated"
        db.add(document)
        db.commit()
        db.refresh(document)
        print("Chunk embeddings generated.")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.exception("Error generating text embeddings for document %s", document.id)
        document.processing_status = "error_text_embeddings"
        db.add(document)
        db.commit()
        raise

    # ======================================
    # FAISS
    # ======================================
    try:
        chunk_ids = [chunk.id for chunk in stored_chunks]
        add_embeddings(
            workspace_id=workspace_id,
            subject_id=subject_id,
            embeddings=embeddings,
            chunk_ids=chunk_ids
        )
        print("Chunk FAISS updated.")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.exception("Error updating FAISS index for document %s", document.id)
        document.processing_status = "error_faiss"
        db.add(document)
        db.commit()
        raise

    # ======================================
    # BM25
    # ======================================
    try:
        bm25_chunks = [{"chunk_id": chunk.id, "text": chunk.text} for chunk in stored_chunks]
        save_bm25_corpus(
            workspace_id=workspace_id,
            subject_id=subject_id,
            chunks=bm25_chunks
        )
        bm25_cache.invalidate(workspace_id=workspace_id, subject_id=subject_id)
        document.processing_status = "bm25_updated"
        db.add(document)
        db.commit()
        db.refresh(document)
        print("BM25 updated.")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.exception("Error updating BM25 for document %s", document.id)
        document.processing_status = "error_bm25"
        db.add(document)
        db.commit()
        raise

    # ======================================
    # FIGURE CAPTION INDEX
    # ======================================
    try:
        index_figure_captions(
            workspace_id=workspace_id,
            subject_id=subject_id,
            figures=stored_figures
        )
        document.processing_status = "captions_indexed"
        db.add(document)
        db.commit()
        db.refresh(document)
        print(f"Figure captions indexed: {len(stored_figures)}")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.exception("Error indexing figure captions for document %s", document.id)
        document.processing_status = "error_captions"
        db.add(document)
        db.commit()
        raise

    # ======================================
    # FIGURE IMAGE INDEX
    # ======================================
    try:
        index_figure_images(
            workspace_id=workspace_id,
            subject_id=subject_id,
            figures=stored_figures
        )
        document.processing_status = "images_indexed"
        db.add(document)
        db.commit()
        db.refresh(document)
        print(f"Figure images indexed: {len(stored_figures)}")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.exception("Error indexing figure images for document %s", document.id)
        document.processing_status = "error_images"
        db.add(document)
        db.commit()
        raise

    document.processing_status = "ready"
    db.add(document)
    db.commit()
    db.refresh(document)

    print("\n========== INGESTION COMPLETE ==========\n")

    return {
        "sections": len(sections),
        "chunks": len(stored_chunks),
        "figures": len(stored_figures)
    }


def ingest_document_by_id(
    document_id: str,
    workspace_id: str,
    subject_id: str
):

    db = SessionLocal()

    try:

        document = db.get(
            Document,
            document_id
        )

        if document is None:

            print(
                f"Document not found for ingestion: "
                f"{document_id}"
            )

            return None

        return ingest_document(
            document=document,
            workspace_id=workspace_id,
            subject_id=subject_id,
            db=db
        )

    except Exception:

        db.rollback()

        raise

    finally:

        db.close()