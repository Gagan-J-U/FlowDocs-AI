from sqlalchemy.orm import Session

from app.models.figure import Figure

from app.embeddings.embedding_service import (
    generate_embedding
)

from app.vision.siglip_text_embedding_service import (
    generate_siglip_text_embedding
)

from app.vectorstore.figure_caption_faiss import (
    search_caption_index
)

from app.vectorstore.figure_image_faiss import (
    search_image_index
)

from app.rag.figure_rank_fusion import (
    reciprocal_rank_fusion
)


def retrieve_figures(

    db: Session,

    workspace_id: str,

    subject_id: str,

    query: str,

    top_k: int = 5
):

    # ----------------------------------
    # Caption Search (BGE)
    # ----------------------------------

    caption_query_embedding = (
        generate_embedding(
            query
        )
    )

    caption_results = (
        search_caption_index(

            workspace_id=workspace_id,

            subject_id=subject_id,

            query_embedding=
            caption_query_embedding,

            top_k=20
        )
    )

    # ----------------------------------
    # Image Search (SigLIP)
    # ----------------------------------

    image_query_embedding = (
        generate_siglip_text_embedding(
            query
        )
    )

    image_results = (
        search_image_index(

            workspace_id=workspace_id,

            subject_id=subject_id,

            query_embedding=
            image_query_embedding,

            top_k=20
        )
    )

    # ----------------------------------
    # Fusion
    # ----------------------------------

    fused_results = (
        reciprocal_rank_fusion(

            caption_results,

            image_results
        )
    )

    figure_ids = [

        figure_id

        for figure_id, _ in fused_results[
            :top_k
        ]
    ]

    if not figure_ids:
        return []

    figures = (

        db.query(Figure)

        .filter(
            Figure.id.in_(
                figure_ids
            )
        )

        .all()
    )

    figure_map = {

        figure.id: figure

        for figure in figures
    }

    results = []

    for figure_id in figure_ids:

        figure = figure_map.get(
            figure_id
        )

        if not figure:
            continue

        results.append({

            "figure_id":
            figure.id,

            "page_number":
            figure.page_number,

            "caption":
            figure.caption,

            "image_path":
            figure.image_path,

            "width":
            figure.width,

            "height":
            figure.height
        })

    return results