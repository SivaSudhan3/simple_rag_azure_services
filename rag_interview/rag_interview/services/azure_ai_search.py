import asyncio

from azure.search.documents.aio import SearchClient
from azure.core.credentials import AzureKeyCredential

from rag_interview.core.config.config import search_settings


class AzureSearchService:

    def __init__(self):

        self.client = SearchClient(
            endpoint=search_settings.AZURE_SEARCH_ENDPOINT,
            index_name="documents-index",
            credential=AzureKeyCredential(
                search_settings.AZURE_SEARCH_KEY
            ),
        )

        # Maximum concurrent uploads
        self.upload_semaphore = asyncio.Semaphore(3)

    async def _upload_batch(
        self,
        documents,
    ):

        async with self.upload_semaphore:

            print(
                f"Uploading batch of {len(documents)} documents..."
            )

            results = await self.client.upload_documents(
                documents
            )

            success = sum(
                1
                for result in results
                if result.succeeded
            )

            print(
                f"Uploaded {success}/{len(documents)} documents"
            )

    async def index_chunks(
        self,
        chunks,
        vectors,
    ):

        

        documents = []

        for chunk, vector in zip(
            chunks,
            vectors,
        ):

            documents.append(
                {
                    "id": chunk.id,
                    "content": chunk.content,
                    "embedding": vector,
                    "chunk_type": chunk.chunk_type,
                    "parent_id": chunk.parent_id,
                    "metadata": str(chunk.metadata),
                }
            )


        
     

        batch_size = 100

        tasks = []

        for i in range(
            0,
            len(documents),
            batch_size,
        ):

            batch = documents[
                i : i + batch_size
            ]

            tasks.append(
                self._upload_batch(batch)
            )

        print(
            f"Uploading {len(documents)} documents "
            f"in {len(tasks)} batches..."
        )

        await asyncio.gather(*tasks)

        print(
            "Azure Search indexing completed."
        )

    async def semantic_rerank(
        self,
        query,
        documents,
        top_k=5,
    ):

        ids = [
            doc["id"]
            for doc in documents
        ]

        filter_expression = " or ".join(
            [
                f"id eq '{id}'"
                for id in ids
            ]
        )

        results = await self.client.search(
            search_text=query,
            query_type="semantic",
            semantic_configuration_name="reranker",
            filter=filter_expression,
            top=top_k,
        )

        return [
            doc
            async for doc in results
        ]

    async def get_document(
        self,
        doc_id,
    ):

        return await self.client.get_document(
            key=doc_id
        )