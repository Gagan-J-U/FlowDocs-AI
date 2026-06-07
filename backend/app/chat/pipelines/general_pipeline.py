from app.llm.factory import (
    get_llm_provider
)


class GeneralPipeline:

    def run(

        self,

        db=None,

        workspace_id=None,

        subject_id=None,

        query: str = "",

        mode: str = "default",

        provider: str = "ollama"
    ):

        llm = get_llm_provider(
            provider
        )

        answer = llm.generate(
            query
        )

        return {

            "answer": answer,

            "citations": [],

            "sources": []
        }