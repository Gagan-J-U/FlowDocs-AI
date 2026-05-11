import re


def clean_text(text: str) -> str:

    # Normalize Windows/Mac line endings
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove excessive spaces/tabs
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove leading/trailing spaces per line
    lines = [
        line.strip()
        for line in text.split("\n")
    ]

    # Remove empty repeated lines
    cleaned_lines = []

    previous_empty = False

    for line in lines:

        if not line:

            if not previous_empty:
                cleaned_lines.append(line)

            previous_empty = True

        else:

            cleaned_lines.append(line)

            previous_empty = False

    text = "\n".join(cleaned_lines)

    return text.strip()