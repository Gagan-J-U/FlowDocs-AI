import re


# ==========================================
# IGNORED SECTION TITLES
# ==========================================

IGNORED_SECTIONS = [

    "contents",
    "table of contents",

    "copyright",
    "copyright page",

    "title page",

    "dedication",
    "acknowledgements",
    "acknowledgments",

    "about the author",
    "about this book",
    "about this ebook",

    "index",
    "glossary",

    "preface",
    "foreword",

    "references",
    "bibliography",
]


# ==========================================
# MINIMUM QUALITY THRESHOLDS
# ==========================================

MIN_WORD_COUNT = 40

MIN_CHARACTER_COUNT = 200


# ==========================================
# DETECT NOISE SECTION
# ==========================================

def is_ignored_section(section_title):

    if not section_title:
        return False

    cleaned_title = (
        section_title
        .strip()
        .lower()
    )

    for ignored in IGNORED_SECTIONS:

        if ignored in cleaned_title:
            return True

    return False


# ==========================================
# DETECT LOW QUALITY TEXT
# ==========================================

def is_low_quality_chunk(text):

    text = text.strip()

    # Too short
    if len(text) < MIN_CHARACTER_COUNT:
        return True

    # Too few words
    if len(text.split()) < MIN_WORD_COUNT:
        return True

    # Excessive symbols/noise
    noisy_characters = re.findall(
        r"[^a-zA-Z0-9\s\.,;:\-\(\)]",
        text
    )

    noise_ratio = (
        len(noisy_characters)
        / max(len(text), 1)
    )

    if noise_ratio > 0.30:
        return True

    return False


# ==========================================
# MAIN FILTER PIPELINE
# ==========================================

def filter_chunks(chunks):

    filtered_chunks = []

    removed_count = 0

    for chunk in chunks:

        section_title = chunk.get(
            "section_title"
        )

        chunk_text = chunk.get(
            "text",
            ""
        )

        # Ignore bad sections
        if is_ignored_section(
            section_title
        ):

            removed_count += 1
            continue

        # Ignore weak chunks
        if is_low_quality_chunk(
            chunk_text
        ):

            removed_count += 1
            continue

        filtered_chunks.append(chunk)

    return filtered_chunks