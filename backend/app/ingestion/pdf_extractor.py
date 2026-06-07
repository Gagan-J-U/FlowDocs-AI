import os
import re
import fitz


# ==========================================
# TOC EXTRACTION
# ==========================================

def extract_toc(document):

    toc = document.get_toc()

    structured_toc = []

    for item in toc:

        level, title, page = item

        structured_toc.append({
            "level": level,
            "title": title.strip(),
            "page": page
        })

    return structured_toc


# ==========================================
# PDF CONTENT EXTRACTION
# ==========================================

def extract_pdf_content(
    pdf_path: str,
    image_output_dir: str
):

    document = fitz.open(pdf_path)

    toc = extract_toc(document)

    extracted_pages = []

    extracted_images = []

    os.makedirs(
        image_output_dir,
        exist_ok=True
    )

    # ==========================================
    # PROCESS PAGES
    # ==========================================

    for page_index in range(len(document)):

        page = document[page_index]

        page_number = page_index + 1

        # ==========================================
        # LAYOUT-AWARE TEXT EXTRACTION
        # ==========================================

        page_dict = page.get_text("dict")

        page_lines = []

        full_page_text = []

        for block in page_dict["blocks"]:

            if "lines" not in block:
                continue

            for line in block["lines"]:

                line_text = ""

                max_font_size = 0

                is_bold = False

                for span in line["spans"]:

                    span_text = span["text"]

                    line_text += span_text + " "

                    # Track largest font size
                    if span["size"] > max_font_size:
                        max_font_size = span["size"]

                    # Detect bold fonts
                    if "bold" in span["font"].lower():
                        is_bold = True

                cleaned_line = line_text.strip()

                if not cleaned_line:
                    continue

                page_lines.append({
                    "text": cleaned_line,
                    "font_size": max_font_size,
                    "is_bold": is_bold
                })

                full_page_text.append(
                    cleaned_line
                )

        full_page_text = "\n".join(
            full_page_text
        )

        extracted_pages.append({
            "page_number": page_number,
            "text": full_page_text,
            "lines": page_lines
        })

        # ==========================================
        # FIGURE DETECTION
        # ==========================================

        figure_matches = re.findall(
            r"\b(?:Figure|Fig\.?|FIGURE|FIG)\s+\d+(?:\.\d+)*",
            full_page_text,
            re.IGNORECASE
        )

        detected_figures = list(
            set(figure_matches)
        )

        # ==========================================
        # IMAGE EXTRACTION
        # ==========================================

        image_list = page.get_images(
            full=True
        )

        for image_index, image in enumerate(image_list):

            xref = image[0]

            base_image = document.extract_image(
                xref
            )

            width = base_image["width"]

            height = base_image["height"]

            # Filter tiny garbage images
            if width < 120 or height < 120:
                continue

            image_bytes = base_image["image"]

            # Filter tiny assets/icons
            if len(image_bytes) < 5000:
                continue

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

                "figure_index": image_index,

                "image_filename": image_filename,

                "image_path": image_path,

                "width": width,

                "height": height,

                "detected_figures": detected_figures,

                "nearby_text": full_page_text[:2000]
            })

    document.close()

    return {
        "toc": toc,
        "pages": extracted_pages,
        "images": extracted_images
    }