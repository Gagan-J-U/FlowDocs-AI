from app.rag.bm25_index import (
    BM25Index
)


class BM25Cache:

    def __init__(self):

        self.cache = {}

    # ==========================================
    # CACHE KEY
    # ==========================================

    def get_key(

        self,

        workspace_id: str,

        subject_id: str
    ):

        return (
            f"{workspace_id}:{subject_id}"
        )

    # ==========================================
    # GET INDEX
    # ==========================================

    def get_index(

        self,

        workspace_id: str,

        subject_id: str
    ):

        key = self.get_key(

            workspace_id,

            subject_id
        )

        # Lazy load index
        if key not in self.cache:

            self.cache[key] = BM25Index(

                workspace_id=workspace_id,

                subject_id=subject_id
            )

        return self.cache[key]

    # ==========================================
    # INVALIDATE CACHE
    # ==========================================

    def invalidate(

        self,

        workspace_id: str,

        subject_id: str
    ):

        key = self.get_key(

            workspace_id,

            subject_id
        )

        if key in self.cache:

            del self.cache[key]


bm25_cache = BM25Cache()