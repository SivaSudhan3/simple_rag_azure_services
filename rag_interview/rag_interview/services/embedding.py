import logging
import time

from langchain_openai import AzureOpenAIEmbeddings
from rag_interview.core.config.config import open_ai_settings

logger = logging.getLogger(__name__)


class EmbeddingService:

    def __init__(self):

        self.model = AzureOpenAIEmbeddings(

            azure_endpoint=open_ai_settings.AZURE_OPENAI_ENDPOINT,

            api_key=open_ai_settings.AZURE_OPENAI_API_KEY,

            azure_deployment=open_ai_settings.AZURE_OPENAI_EMBEDDING_DEPLOYMENT,

            api_version=open_ai_settings.AZURE_OPENAI_API_VERSION,

        )
        logger.info(id(self.model.async_client))

    async def embed_text(
        self,
        text,
    ):

        start = time.perf_counter()

        vector = await self.model.aembed_query(text)

        logger.info(
            "EMBEDDING API : %.3f sec",
            time.perf_counter() - start,
        )

        return vector

    async def embed_documents(
        self,
        chunks,
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

        start = time.perf_counter()

        vectors = await self.model.aembed_documents(
            texts
        )

        logger.info(
            "DOCUMENT EMBEDDINGS : %.3f sec | Chunks=%d",
            time.perf_counter() - start,
            len(texts),
        )

        return valid_chunks, vectors