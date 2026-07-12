
class Reranker:

    def __init__(self, search_service):
        self.search_service = search_service

    async def rerank(
        self,
        query,
        documents
    ):
        return await self.search_service.semantic_rerank(
            query,
            documents
        )