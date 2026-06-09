import numpy as np

from app.models.figure import Figure

from app.vectorstore.figure_image_faiss import (
    add_image_embeddings
)


def index_figure_images(

    workspace_id: str,

    subject_id: str,

    figures: list[Figure]
):

    image_paths = []
    image_ids = []

    for figure in figures:

        if not figure.image_path:
            continue

        image_paths.append(
            figure.image_path
        )

        image_ids.append(
            figure.id
        )

    if not image_paths:
        return

    # Import image embedding service only when needed
    from app.vision.image_embedding_service import (
        generate_image_embeddings
    )

    embeddings = (
        generate_image_embeddings(
            image_paths,
            batch_size=16
        )
    )

    add_image_embeddings(

        workspace_id=workspace_id,

        subject_id=subject_id,

        embeddings=np.array(
            embeddings,
            dtype=np.float32
        ),

        figure_ids=image_ids
    )