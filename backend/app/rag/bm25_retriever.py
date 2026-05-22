from rank_bm25 import BM25Okapi


class BM25Retriever:

    def __init__(self):

        self.bm25 = None

        self.chunk_lookup = []

    def build_index(
        self,
        chunks: list
    ):

        tokenized_chunks = []

        self.chunk_lookup = []

        for chunk in chunks:

            text = chunk["text"]

            tokens = text.lower().split()

            tokenized_chunks.append(tokens)

            self.chunk_lookup.append({

                "chunk_id": chunk["chunk_id"],

                "text": text
            })

        self.bm25 = BM25Okapi(
            tokenized_chunks
        )

    def search(
        self,
        query: str,
        top_k: int = 10
    ):

        if not self.bm25:
            return []

        tokenized_query = (
            query.lower().split()
        )

        scores = self.bm25.get_scores(
            tokenized_query
        )

        scored_results = []

        for idx, score in enumerate(scores):

            result = self.chunk_lookup[idx]

            scored_results.append({

                "chunk_id": result["chunk_id"],

                "text": result["text"],

                "bm25_score": float(score)
            })

        scored_results.sort(

            key=lambda x: x["bm25_score"],

            reverse=True
        )

        return scored_results[:top_k]


bm25_retriever = BM25Retriever()