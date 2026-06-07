from app.rag.document_retriever import (
    retrieve_document_chunks
)

from app.comparison.document_summarizer import (
    summarize_document_context
)

from app.llm.factory import (
    get_llm_provider
)
from app.rag.figure_retriever import(
    retrieve_figures
)


class ComparisonPipeline:

    def run(
        self,
        db,
        workspace_id: str,
        subject_id: str,
        document_a_id: str,
        document_b_id: str,
        query: str,
        provider: str = "ollama"
    ):

        figures = retrieve_figures(

            db=db,

            workspace_id=workspace_id,

            subject_id=subject_id,

            query=query,

            top_k=5
        )

        figure_context = ""

        if figures:

            blocks = []

            for index, figure in enumerate(figures):

                blocks.append(
                    f"""
        [Figure {index + 1}]

        Figure ID:
        {figure["figure_id"]}

        Page:
        {figure["page_number"]}

        Caption:
        {figure["caption"]}
        """
                )

            figure_context = "\n".join(
                blocks
            )
        # ==========================================
        # Retrieve Relevant Chunks
        # ==========================================

        chunks_a = retrieve_document_chunks(

            db=db,

            workspace_id=workspace_id,

            subject_id=subject_id,

            document_id=document_a_id,

            query=query,

            top_k=15
        )

        chunks_b = retrieve_document_chunks(

            db=db,

            workspace_id=workspace_id,

            subject_id=subject_id,

            document_id=document_b_id,

            query=query,

            top_k=15
        )

        # ==========================================
        # Build Document Summaries
        # ==========================================

        summary_a = summarize_document_context(

            chunks=chunks_a,

            provider=provider
        )

        summary_b = summarize_document_context(

            chunks=chunks_b,

            provider=provider
        )

        # ==========================================
        # Comparison Prompt
        # ==========================================

        prompt = f"""
You are an expert document analyst.

QUESTION:

{query}

--------------------------------------------------

DOCUMENT A SUMMARY

{summary_a}

--------------------------------------------------

DOCUMENT B SUMMARY

{summary_b}

--------------------------------------------------

AVAILABLE FIGURES:

{figure_context}

--------------------------------------------------

Compare the two documents and provide:

1. Executive Summary

2. Similarities

3. Differences

4. Strengths of Document A

5. Strengths of Document B

6. Key Insights

7. Final Conclusion

Only use information from the provided summaries.
"""

        # ==========================================
        # Generate Comparison
        # ==========================================

        llm = get_llm_provider(
            provider
        )

        answer = llm.generate(
            prompt
        )

        # ==========================================
        # Return Result
        # ==========================================

        return {

            "query": query,

            "answer": answer,

            "document_a_id": document_a_id,

            "document_b_id": document_b_id,

            "document_a_summary": summary_a,

            "document_b_summary": summary_b,

            "document_a_sources": chunks_a,

            "document_b_sources": chunks_b,

            "figures": figures
        }