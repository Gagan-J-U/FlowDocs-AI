import os
import re
import fitz


def extract_pdf_content(
    pdf_path: str,
    image_output_dir: str
):

    document = fitz.open(pdf_path)

    extracted_pages = []

    extracted_images = []

    os.makedirs(
        image_output_dir,
        exist_ok=True
    )

    for page_index in range(len(document)):

        page = document[page_index]

        page_number = page_index + 1

        # =========================
        # Extract Text
        # =========================

        text = page.get_text()

        extracted_pages.append({
            "page_number": page_number,
            "text": text
        })

        # =========================
        # Find Figure References
        # =========================

        figure_matches = re.findall(
            r"\b(?:Figure|Fig\.?|FIGURE|FIG)\s+\d+(?:\.\d+)*",
            text,
            re.IGNORECASE
        )

        detected_figures = list(
            set(figure_matches)
        )

        # =========================
        # Extract Images
        # =========================

        image_list = page.get_images(
            full=True
        )

        for image_index, image in enumerate(image_list):

            xref = image[0]

            base_image = document.extract_image(
                xref
            )

            image_bytes = base_image["image"]

            image_ext = base_image["ext"]

            image_filename = (
                f"page_{page_number}_img_{image_index}.{image_ext}"
            )

            image_path = os.path.join(
                image_output_dir,
                image_filename
            )

            with open(image_path, "wb") as img_file:
                img_file.write(image_bytes)

            extracted_images.append({
                "page_number": page_number,
                "image_filename": image_filename,
                "image_path": image_path,
                "detected_figures": detected_figures
            })

    document.close()

    return {
        "pages": extracted_pages,
        "images": extracted_images
    }