from sqlalchemy.orm import Session

from app.models.chunk import Chunk


def get_document_chunks(

    db: Session,

    document_id: str
):

    chunks = (

        db.query(Chunk)

        .filter(
            Chunk.document_id == document_id
        )

        .all()
    )

    return chunks