def recall_at_k(
    retrieved_ids,
    expected_ids,
    k
):

    retrieved = set(
        retrieved_ids[:k]
    )

    expected = set(
        expected_ids
    )

    if not expected:
        return 0

    hits = len(
        retrieved.intersection(
            expected
        )
    )

    return hits / len(expected)


def precision_at_k(
    retrieved_ids,
    expected_ids,
    k
):

    retrieved = set(
        retrieved_ids[:k]
    )

    expected = set(
        expected_ids
    )

    if not retrieved:
        return 0

    hits = len(
        retrieved.intersection(
            expected
        )
    )

    return hits / len(retrieved)


def mean_reciprocal_rank(
    retrieved_ids,
    expected_ids
):

    for rank, chunk_id in enumerate(
        retrieved_ids,
        start=1
    ):

        if chunk_id in expected_ids:

            return 1 / rank

    return 0