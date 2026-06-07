import numpy as np

from app.models.figure import Figure

from app.embeddings.embedding_service import (
    generate_embedding
)

from app.vision.image_embedding_service import (
    generate_image_embedding
)

from app.vectorstore.figure_caption_faiss import (
    add_caption_embeddings
)

from app.vectorstore.figure_image_faiss import (
    add_image_embeddings
)


def index_figures(

    workspace_id: str,

    subject_id: str,

    figures: list[Figure]
):

    caption_embeddings = []

    caption_ids = []

    image_embeddings = []

    image_ids = []

    for figure in figures:

        # --------------------------
        # Caption Embeddings
        # --------------------------

        if figure.caption:

            caption_embedding = (
                generate_embedding(
                    figure.caption
                )
            )

            caption_embeddings.append(
                caption_embedding
            )

            caption_ids.append(
                figure.id
            )

        # --------------------------
        # Image Embeddings
        # --------------------------

        try:

            image_embedding = (
                generate_image_embedding(
                    figure.image_path
                )
            )

            image_embeddings.append(
                image_embedding
            )

            image_ids.append(
                figure.id
            )

        except Exception as e:

            print(
                f"Image embedding failed "
                f"for {figure.id}: {e}"
            )

    # --------------------------
    # Caption Index
    # --------------------------

    if caption_embeddings:

        add_caption_embeddings(

            workspace_id=workspace_id,

            subject_id=subject_id,

            embeddings=np.array(
                caption_embeddings,
                dtype=np.float32
            ),

            figure_ids=caption_ids
        )

    # --------------------------
    # Image Index
    # --------------------------

    if image_embeddings:

        add_image_embeddings(

            workspace_id=workspace_id,

            subject_id=subject_id,

            embeddings=np.array(
                image_embeddings,
                dtype=np.float32
            ),

            figure_ids=image_ids
        )