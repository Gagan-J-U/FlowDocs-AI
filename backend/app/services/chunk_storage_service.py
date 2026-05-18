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

        db.add(db_chunk)

        stored_chunks.append(
            db_chunk
        )

    # Commit once for efficiency
    db.commit()

    # Refresh to get generated UUIDs
    for chunk in stored_chunks:

        db.refresh(chunk)

    return stored_chunks