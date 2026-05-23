from sqlalchemy.orm import Session

from app.models.chunk import Chunk


# ==========================================
# STORE CHUNKS IN DATABASE
# ==========================================

def store_chunks(

    chunks,

    document_id: str,

    db: Session
):

    stored_chunks = []

    for chunk in chunks:

        db_chunk = Chunk(

            chunk_index=chunk["chunk_index"],

            text=chunk["text"],

            section_title=chunk[
                "section_title"
            ],

            parent_section=chunk[
                "parent_section"
            ],

            hierarchy_level=chunk[
                "hierarchy_level"
            ],

            start_page=chunk[
                "start_page"
            ],

            end_page=chunk[
                "end_page"
            ],

            document_id=document_id
        )

        stored_chunks.append(
            db_chunk
        )

    db.add_all(stored_chunks)

    # Flush once so generated UUIDs are available without per-row refreshes.
    db.flush()

    db.commit()

    return stored_chunks
