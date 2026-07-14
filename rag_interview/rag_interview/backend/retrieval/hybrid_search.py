import asyncio
import logging
import time

from azure.search.documents.models import VectorizedQuery

logger = logging.getLogger(__name__)


class HybridSearcher:

    def __init__(
        self,
        search_client,
        embedding_service,
    ):

        self.client = search_client
        self.embedding = embedding_service

    async def vector_search_from_embedding(
        self,
        embedding,
        telemetry=None,
        top_k=10,
    ):

        start = time.perf_counter()

        vector_query = VectorizedQuery(
            vector=embedding,
            fields="embedding",
            k_nearest_neighbors=top_k,
        )

        # -------------------------
        # Azure Search API
        # -------------------------

        api_start = time.perf_counter()

        results = await self.client.search(
            search_text=None,
            vector_queries=[vector_query],
            top=top_k,
            select=[
                "id",
                "content",
                "metadata",
                "parent_id"
            ],
        )

        api_end = time.perf_counter()

        docs = [
            doc
            async for doc in results
        ]

        deserialize_end = time.perf_counter()

        if telemetry:
            telemetry.timings.vector_search_ms = (
                deserialize_end - start
            ) * 1000

            telemetry.retrieval.vector_results = len(
                docs
            )

        logger.info(
            "Vector API         : %.3f sec",
            api_end - api_start,
        )

        logger.info(
            "Vector Deserialize : %.3f sec",
            deserialize_end - api_end,
        )

        logger.info(
            "Vector Search      : %.3f sec",
            deserialize_end - start,
        )

        return docs

    async def lexical_search(
        self,
        query,
        telemetry=None,
        top_k=5,
    ):

        start = time.perf_counter()

        # -------------------------
        # Azure Search API
        # -------------------------

        api_start = time.perf_counter()

        results = await self.client.search(
            search_text=query,
            search_fields=["content"],
            search_mode="any",
            top=top_k,
            select=[
                "id",
                "content",
                "metadata",
                "parent_id"
            ],
        )

        api_end = time.perf_counter()

        docs = [
            doc
            async for doc in results
        ]

        deserialize_end = time.perf_counter()

        if telemetry:
            telemetry.timings.lexical_search_ms = (
                deserialize_end - start
            ) * 1000

            telemetry.retrieval.lexical_results = len(
                docs
            )

        logger.info(
            "Lexical API        : %.3f sec",
            api_end - api_start,
        )

        logger.info(
            "Lexical Deserialize: %.3f sec",
            deserialize_end - api_end,
        )

        logger.info(
            "Lexical Search     : %.3f sec",
            deserialize_end - start,
        )

        return docs

    async def search(
        self,
        query,
        telemetry=None,
    ):

        overall = time.perf_counter()

        # ----------------------------------------
        # Run embedding and lexical together
        # ----------------------------------------

        embedding_start = time.perf_counter()

        embedding_task = asyncio.create_task(
            self.embedding.embed_text(query)
        )

        lexical_task = asyncio.create_task(
            self.lexical_search(
                query,
                telemetry=telemetry,
            )
        )

        embedding, lexical = await asyncio.gather(
            embedding_task,
            lexical_task,
        )

        embedding_time = (
            time.perf_counter() - embedding_start
        )

        if telemetry:
            telemetry.timings.embedding_ms = (
                embedding_time * 1000
            )

        logger.info(
            "Embedding          : %.3f sec",
            embedding_time,
        )

        # ----------------------------------------
        # Vector Search
        # ----------------------------------------

        vector = await self.vector_search_from_embedding(
            embedding,
            telemetry=telemetry,
        )

        logger.info(
            "TOTAL Hybrid Search: %.3f sec",
            time.perf_counter() - overall,
        )

        return [
            vector,
            lexical,
        ]