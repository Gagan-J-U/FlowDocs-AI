import re


def extract_figure_ids(
    answer: str
):

    pattern = (
        r"\[FIGURE:(.*?)\]"
    )

    return re.findall(
        pattern,
        answer
    )