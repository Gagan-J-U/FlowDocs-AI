from app.chat.pipelines.rag_pipeline import (
    RAGPipeline
)

from app.chat.pipelines.general_pipeline import (
    GeneralPipeline
)


class ChatOrchestrator:

    def __init__(self):

        self.rag_pipeline = (
            RAGPipeline()
        )

        self.general_pipeline = (
            GeneralPipeline()
        )

    def handle(

        self,

        chat_type,

        **kwargs
    ):

        if chat_type == "general":

            return self.general_pipeline.run(
                **kwargs
            )

        return self.rag_pipeline.run(
            **kwargs
        )


orchestrator = ChatOrchestrator()