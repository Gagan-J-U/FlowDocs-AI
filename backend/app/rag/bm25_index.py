import os
import pickle
import re
import heapq

from rank_bm25 import BM25Okapi


VECTOR_STORAGE_DIR = "vector_storage"


class BM25Index:

    def __init__(

        self,

        workspace_id: str,

        subject_id: str
    ):

        self.corpus = []

        self.bm25 = None

        subject_path = os.path.join(

            VECTOR_STORAGE_DIR,

            str(workspace_id),

            str(subject_id)
        )

        corpus_path = os.path.join(

            subject_path,

            "bm25_corpus.pkl"
        )

        index_path = os.path.join(

            subject_path,

            "bm25_index.pkl"
        )

        # No corpus yet
        if not os.path.exists(corpus_path):

            return

        # Load persisted corpus
        with open(corpus_path, "rb") as file:

            self.corpus = pickle.load(file)

        if (
            os.path.exists(index_path)
            and os.path.getmtime(index_path) >= os.path.getmtime(corpus_path)
        ):

            with open(index_path, "rb") as file:

                self.bm25 = pickle.load(file)

            return

        # Tokenize corpus
        tokenized_corpus = [

            self.tokenize(chunk["text"])

            for chunk in self.corpus
        ]

        # Build BM25 index
        self.bm25 = BM25Okapi(
            tokenized_corpus
        )

        with open(index_path, "wb") as file:

            pickle.dump(
                self.bm25,
                file
            )

    # ==========================================
    # TOKENIZER
    # ==========================================

    def tokenize(
        self,
        text: str
    ):

        return re.findall(

            r"\w+",

            text.lower()
        )

    # ==========================================
    # SEARCH
    # ==========================================

    def search(

        self,

        query: str,

        top_k: int = 10
    ):

        if not self.bm25:

            return []

        tokenized_query = self.tokenize(
            query
        )

        scores = self.bm25.get_scores(
            tokenized_query
        )

        top_results = heapq.nlargest(
            top_k,
            enumerate(scores),
            key=lambda item: item[1]
        )

        scored_results = []

        for idx, score in top_results:

            chunk = self.corpus[idx]

            scored_results.append({

                "chunk_id": chunk["chunk_id"],

                "text": chunk["text"],

                "bm25_score": float(score)
            })

        return scored_results
