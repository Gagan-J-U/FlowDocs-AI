import re

from app.ingestion.text_cleaner import clean_text


# ==========================================
# REGEX HEADING PATTERNS
# ==========================================

HEADING_PATTERNS = [
    r"^\d+(\.\d+)*\s+.+",
    r"^(Chapter|CHAPTER)\s+\d+",
    r"^[A-Z][A-Z\s\-\&]{5,}$",
]


# ==========================================
# REGEX HEADING DETECTION
# ==========================================

def is_regex_heading(text: str) -> bool:

    text = text.strip()

    for pattern in HEADING_PATTERNS:

        if re.match(pattern, text):
            return True

    return False


# ==========================================
# REGEX HIERARCHY LEVEL
# ==========================================

def get_regex_level(text: str):

    match = re.match(
        r"^(\d+(\.\d+)*)",
        text
    )

    if not match:
        return 1

    numbering = match.group(1)

    return numbering.count(".") + 1


# ==========================================
# LAYOUT HEADING DETECTION
# ==========================================

def is_layout_heading(line_data):

    text = line_data["text"].strip()

    font_size = line_data.get(
        "font_size",
        0
    )

    is_bold = line_data.get(
        "is_bold",
        False
    )

    # Large font
    if font_size >= 15:
        return True

    # Bold uppercase
    if is_bold and text.isupper():
        return True

    # Short bold title
    if is_bold and len(text.split()) <= 8:
        return True

    return False


# ==========================================
# LAYOUT HIERARCHY LEVEL
# ==========================================

def get_layout_level(line_data):

    font_size = line_data.get(
        "font_size",
        12
    )

    if font_size >= 22:
        return 1

    if font_size >= 18:
        return 2

    if font_size >= 15:
        return 3

    return 4


# ==========================================
# TOC PAGE BOUNDARIES
# ==========================================

def build_toc_boundaries(toc):

    if not toc:
        return []

    boundaries = []

    hierarchy_stack = {}

    for index, item in enumerate(toc):

        title = item["title"]

        level = item["level"]

        start_page = item["page"]

        # Track hierarchy
        hierarchy_stack[level] = title

        # Remove deeper stale levels
        stale_levels = [
            key
            for key in hierarchy_stack
            if key > level
        ]

        for stale_level in stale_levels:
            del hierarchy_stack[stale_level]

        # Parent section
        parent_title = hierarchy_stack.get(
            level - 1
        )

        # Determine end page
        if index == len(toc) - 1:

            end_page = 999999

        else:

            end_page = (
                toc[index + 1]["page"] - 1
            )

        boundaries.append({
            "title": title,
            "level": level,
            "parent_title": parent_title,
            "start_page": start_page,
            "end_page": end_page
        })

    return boundaries


# ==========================================
# FIND TOC SECTION
# ==========================================

def get_toc_section(
    page_number,
    toc_boundaries
):

    for section in toc_boundaries:

        if (
            section["start_page"]
            <= page_number
            <= section["end_page"]
        ):

            return section

    return None


# ==========================================
# FINALIZE SECTION
# ==========================================

def finalize_section(section):

    section["content"] = "\n".join(
        section["content"]
    ).strip()

    return section


# ==========================================
# MAIN HYBRID SECTION BUILDER
# ==========================================

def build_sections(
    extracted_pages,
    toc=None
):

    sections = []

    toc_boundaries = build_toc_boundaries(
        toc
    )

    hierarchy_stack = {}

    current_section = {
        "title": "Introduction",
        "level": 1,
        "parent_title": None,
        "content": [],
        "start_page": 1,
        "end_page": 1
    }

    current_toc_title = None

    # ==========================================
    # PROCESS PAGES
    # ==========================================

    for page in extracted_pages:

        page_number = page["page_number"]

        page_lines = page["lines"]

        # ==========================================
        # TOC SECTION DETECTION
        # ==========================================

        toc_section = get_toc_section(
            page_number,
            toc_boundaries
        )

        if (
            toc_section
            and toc_section["title"]
            != current_toc_title
        ):

            if current_section["content"]:

                sections.append(
                    finalize_section(
                        current_section
                    )
                )

            current_section = {
                "title": toc_section["title"],
                "level": toc_section["level"],
                "parent_title": toc_section[
                    "parent_title"
                ],
                "content": [],
                "start_page": page_number,
                "end_page": page_number
            }

            current_toc_title = (
                toc_section["title"]
            )

        # ==========================================
        # PROCESS LINES
        # ==========================================

        for line_data in page_lines:

            raw_text = line_data["text"]

            cleaned_line = clean_text(
                raw_text
            )

            if not cleaned_line:
                continue

            # ==========================================
            # DETECTION
            # ==========================================

            layout_heading = is_layout_heading(
                line_data
            )

            regex_heading = is_regex_heading(
                cleaned_line
            )

            detected_heading = (
                layout_heading
                or regex_heading
            )

            # ==========================================
            # FALLBACK HIERARCHY
            # ==========================================

            if (
                not toc_section
                and detected_heading
            ):

                # Determine hierarchy level
                if regex_heading:

                    level = get_regex_level(
                        cleaned_line
                    )

                else:

                    level = get_layout_level(
                        line_data
                    )

                # Track hierarchy stack
                hierarchy_stack[level] = (
                    cleaned_line
                )

                # Remove stale deeper levels
                stale_levels = [
                    key
                    for key in hierarchy_stack
                    if key > level
                ]

                for stale_level in stale_levels:
                    del hierarchy_stack[
                        stale_level
                    ]

                parent_title = (
                    hierarchy_stack.get(
                        level - 1
                    )
                )

                # Save previous section
                if current_section["content"]:

                    sections.append(
                        finalize_section(
                            current_section
                        )
                    )

                # Start new section
                current_section = {
                    "title": cleaned_line,
                    "level": level,
                    "parent_title": parent_title,
                    "content": [],
                    "start_page": page_number,
                    "end_page": page_number
                }

            else:

                current_section["content"].append(
                    cleaned_line
                )

                current_section["end_page"] = (
                    page_number
                )

    # ==========================================
    # FINAL SECTION
    # ==========================================

    if current_section["content"]:

        sections.append(
            finalize_section(
                current_section
            )
        )

    return sections