from sentence_transformers import CrossEncoder

import torch
import os


class Reranker:

    def __init__(
        self,
        model_name: str = (
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )
    ):

        self.model = CrossEncoder(
            model_name,
            local_files_only=(
                os.getenv("HF_LOCAL_FILES_ONLY", "1") != "0"
            )
        )

        # Optional GPU optimization
        if torch.cuda.is_available():

            self.model.model.half()

    def rerank(
        self,
        query: str,
        chunks: list,
        top_k: int = 5
    ):

        if not chunks:
            return []

        pairs = [
            [query, chunk["text"]]
            for chunk in chunks
        ]

        scores = self.model.predict(
            pairs,
            batch_size=16,
            show_progress_bar=False
        )

        for chunk, score in zip(chunks, scores):

            chunk["rerank_score"] = float(score)

        reranked_chunks = sorted(

            chunks,

            key=lambda x: x["rerank_score"],

            reverse=True
        )

        return reranked_chunks[:top_k]


reranker = Reranker()
