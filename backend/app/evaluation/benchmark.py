import time

from app.core.database import (
    SessionLocal
)

from app.rag.retriever import (
    retrieve_chunks
)

from app.evaluation.dataset import (
    load_test_queries
)

from app.evaluation.metrics import (
    recall_at_k,
    precision_at_k,
    mean_reciprocal_rank
)


def benchmark(
    workspace_id,
    subject_id
):

    db = SessionLocal()

    dataset = load_test_queries()

    recall5_scores = []
    recall10_scores = []

    precision5_scores = []
    precision10_scores = []

    mrr_scores = []

    latencies = []

    print("\nRunning Benchmark...\n")

    for sample in dataset:

        query = sample["query"]

        expected_ids = sample[
            "expected_chunk_ids"
        ]

        start = time.time()

        results = retrieve_chunks(

            db=db,

            workspace_id=workspace_id,

            subject_id=subject_id,

            query=query,

            top_k=10
        )

        latency = (
            time.time() - start
        )

        retrieved_ids = [

            result["chunk_id"]

            for result in results
        ]

        recall5_scores.append(

            recall_at_k(

                retrieved_ids,

                expected_ids,

                5
            )
        )

        recall10_scores.append(

            recall_at_k(

                retrieved_ids,

                expected_ids,

                10
            )
        )

        precision5_scores.append(

            precision_at_k(

                retrieved_ids,

                expected_ids,

                5
            )
        )

        precision10_scores.append(

            precision_at_k(

                retrieved_ids,

                expected_ids,

                10
            )
        )

        mrr_scores.append(

            mean_reciprocal_rank(

                retrieved_ids,

                expected_ids
            )
        )

        latencies.append(
            latency
        )

        print(
            f"Processed: {query}"
        )

    print("\n========== RESULTS ==========\n")

    print(
        f"Recall@5: "
        f"{sum(recall5_scores)/len(recall5_scores):.4f}"
    )

    print(
        f"Recall@10: "
        f"{sum(recall10_scores)/len(recall10_scores):.4f}"
    )

    print(
        f"Precision@5: "
        f"{sum(precision5_scores)/len(precision5_scores):.4f}"
    )

    print(
        f"Precision@10: "
        f"{sum(precision10_scores)/len(precision10_scores):.4f}"
    )

    print(
        f"MRR: "
        f"{sum(mrr_scores)/len(mrr_scores):.4f}"
    )

    print(
        f"Average Latency: "
        f"{sum(latencies)/len(latencies):.4f}s"
    )

    db.close()