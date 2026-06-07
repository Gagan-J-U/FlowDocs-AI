import json

from app.core.database import (
    SessionLocal
)

from app.rag.retriever import (
    retrieve_chunks
)


WORKSPACE_ID = ""

SUBJECT_ID = ""


def create_dataset():

    db = SessionLocal()

    dataset = []

    while True:

        query = input(
            "\nQuery (or 'exit'): "
        )

        if query.lower() == "exit":

            break

        results = retrieve_chunks(

            db=db,

            workspace_id=WORKSPACE_ID,

            subject_id=SUBJECT_ID,

            query=query,

            top_k=10
        )

        print(
            "\nRetrieved Chunks:\n"
        )

        for idx, chunk in enumerate(
            results
        ):

            print(
                f"\n[{idx}] "
                f"{chunk['chunk_id']}"
            )

            print(
                chunk["text"][:300]
            )

            print(
                "\n" + "-" * 50
            )

        selected = input(
            "\nRelevant indexes (comma separated): "
        )

        indexes = [

            int(i.strip())

            for i in selected.split(",")

            if i.strip()
        ]

        expected_chunk_ids = [

            results[i]["chunk_id"]

            for i in indexes
        ]

        dataset.append({

            "query": query,

            "expected_chunk_ids":
            expected_chunk_ids
        })

    with open(

        "app/evaluation/test_queries.json",

        "w",

        encoding="utf-8"
    ) as file:

        json.dump(

            dataset,

            file,

            indent=4
        )

    print(
        "\nDataset saved."
    )


if __name__ == "__main__":

    create_dataset()