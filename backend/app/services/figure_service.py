from sqlalchemy.orm import Session

from app.models.figure import (
    Figure
)

from app.vision.caption_service import (
    generate_caption
)


def store_figures(

    document_id: str,

    extracted_images: list,

    db: Session
):

    stored_figures = []

    for image in extracted_images:

        caption = generate_caption(

            image["image_path"]
        )

        figure = Figure(

            document_id=document_id,

            page_number=image["page_number"],

            figure_index=image["figure_index"],

            image_filename=image["image_filename"],

            image_path=image["image_path"],

            width=image["width"],

            height=image["height"],

            nearby_text=image.get(
                "nearby_text"
            ),

            caption=caption
        )

        db.add(figure)

        stored_figures.append(
            figure
        )

    db.commit()

    return stored_figures