def merge_results(
    dense_results: list,
    sparse_results: list
):

    merged = {}

    # Add dense results first
    for chunk in dense_results:

        merged[chunk["chunk_id"]] = chunk

    # Merge sparse results
    for chunk in sparse_results:

        chunk_id = chunk["chunk_id"]

        if chunk_id not in merged:

            merged[chunk_id] = chunk

        else:

            merged[chunk_id]["bm25_score"] = (
                chunk["bm25_score"]
            )

    return list(merged.values())