from app.rag.retriever import (
    retrieve_chunks
)

from app.prompting.factory import (
    get_prompt_strategy
)

from app.llm.factory import (
    get_llm_provider
)

from app.services.citation_service import (
    build_citation_block
)

from app.rag.figure_retriever import (
    retrieve_figures
)


class RAGPipeline:

    def run(

        self,

        db,

        workspace_id: str,

        subject_id: str,

        query: str,

        mode: str = "default",

        provider: str = "ollama"
    ):

        # -------------------------
        # Retrieve Chunks
        # -------------------------

        chunks = retrieve_chunks(

            db=db,

            workspace_id=workspace_id,

            subject_id=subject_id,

            query=query,

            top_k=5
        )
        # -------------------------
        # Retrieve Figures
        # -------------------------
        figures = retrieve_figures(

            db=db,

            workspace_id=workspace_id,

            subject_id=subject_id,

            query=query,

            top_k=5
        )

        # -------------------------
        # Prompt Strategy
        # -------------------------

        strategy = get_prompt_strategy(
            mode
        )

        prompt = strategy.build(

            query=query,

            chunks=chunks,

            figures=figures
        )

        # -------------------------
        # LLM
        # -------------------------

        llm = get_llm_provider(
            provider
        )

        answer = llm.generate(
            prompt
        )

        # -------------------------
        # Citations
        # -------------------------

        citations = build_citation_block(
            chunks
        )

        return {

            "answer": answer,

            "citations": citations,

            "sources": chunks,

            "figures": figures
        }