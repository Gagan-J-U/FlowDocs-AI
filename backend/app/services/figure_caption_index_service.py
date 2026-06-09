import numpy as np

from app.models.figure import Figure

from app.embeddings.embedding_service import (
    generate_embeddings
)

from app.vectorstore.figure_caption_faiss import (
    add_caption_embeddings
)


def index_figure_captions(
    workspace_id: str,
    subject_id: str,
    figures: list[Figure]
):

    captions = []
    figure_ids = []

    for figure in figures:
        if not figure.caption:
            continue
        captions.append(figure.caption)
        figure_ids.append(figure.id)

    if not captions:
        return

    embeddings = generate_embeddings(
        captions
    )

    add_caption_embeddings(
        workspace_id=workspace_id,
        subject_id=subject_id,
        embeddings=np.array(
            embeddings,
            dtype=np.float32
        ),
        figure_ids=figure_ids
    )