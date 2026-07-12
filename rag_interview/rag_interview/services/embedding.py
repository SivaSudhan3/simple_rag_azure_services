from langchain_openai import AzureOpenAIEmbeddings
from rag_interview.core.config.config import open_ai_settings
from azure.core.credentials import AzureKeyCredential


class EmbeddingService:


    def __init__(
        self
    ):


        self.model = AzureOpenAIEmbeddings(


            azure_endpoint=
            open_ai_settings.AZURE_OPENAI_ENDPOINT,

            api_key=
            open_ai_settings.AZURE_OPENAI_API_KEY,

            azure_deployment=
            open_ai_settings. AZURE_OPENAI_EMBEDDING_DEPLOYMENT,

            api_version=
            open_ai_settings.AZURE_OPENAI_API_VERSION

        )


    async def embed_text(
        self,
        text
    ):


        vector = (
            await self.model
            .aembed_query(
                text
            )
        )


        return vector



    async def embed_documents(
    self,
    chunks
    ):


        valid_chunks = [
            chunk
            for chunk in chunks
            if chunk.embedding_content
        ]

        texts = [
            chunk.embedding_content
            for chunk in valid_chunks
        ]

        vectors = await self.model.aembed_documents(
            texts
        )

        return valid_chunks, vectors