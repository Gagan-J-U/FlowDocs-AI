def reciprocal_rank_fusion(

    caption_results,

    image_results,

    k=60
):

    scores = {}

    for rank, result in enumerate(
        caption_results,
        start=1
    ):

        figure_id = result[
            "figure_id"
        ]

        scores[figure_id] = (
            scores.get(
                figure_id,
                0
            )
            +
            1 / (k + rank)
        )

    for rank, result in enumerate(
        image_results,
        start=1
    ):

        figure_id = result[
            "figure_id"
        ]

        scores[figure_id] = (
            scores.get(
                figure_id,
                0
            )
            +
            1 / (k + rank)
        )

    return sorted(

        scores.items(),

        key=lambda x: x[1],

        reverse=True
    )