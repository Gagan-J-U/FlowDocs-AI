import json


def load_test_queries(
    path="app/evaluation/test_queries.json"
):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def save_test_queries(
    dataset,
    path="app/evaluation/test_queries.json"
):

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            dataset,
            file,
            indent=4
        )