from azure.search.documents.models import VectorizedQuery


class HybridSearcher:


    def __init__(
        self,
        search_client,
        embedding_service
    ):

        self.client = search_client

        self.embedding = (
            embedding_service
        )


    async def vector_search(
        self,
        query,
        top_k=10
    ):


        vector = (
            await self.embedding
            .embed_text(
                query
            )
        )


        vector_query = VectorizedQuery(

            vector=vector,

            fields="embedding",

            k_nearest_neighbors=top_k

        )


        results = await self.client.search(

            search_text=None,

            vector_queries=[
                vector_query
            ],

            top=top_k

        )


        return [

            doc

            async for doc in results

        ]
    async def lexical_search(
        self,
        query,
        top_k=10
    ):


        results = await self.client.search(

            search_text=query,

            top=top_k

        )


        return [

            doc

            async for doc in results

        ]
    async def search(
        self,
        query
    ):


        vector = (
            await self.vector_search(
                query
            )
        )


        lexical = (
            await self.lexical_search(
                query
            )
        )


        return [
            vector,
            lexical
        ]