from rag_interview.graph.graph_schema import RetrievedDocument
import ast
import asyncio
class Retriever:


    def __init__(
        self,
        expander,
        searcher,
        rrf,
        deduper,
        reranker,
        parent_expander,
        context_builder
    ):


        self.expander=expander

        self.searcher=searcher

        self.rrf=rrf

        self.deduper=deduper
        self.reranker = reranker
        self.parent_expander = parent_expander
        self.context_builder = context_builder



    async def retrieve(
        self,
        question,
        chat_history: list[dict] | None = None,
    ):


        #queries = (await self.expander.expand(question=question,chat_history=chat_history))

        queries = [question]

        all_results=[]



        tasks = [
            self.searcher.search(query)
            for query in queries
        ]

        results = await asyncio.gather(*tasks)

        all_results = []

        for docs in results:
            all_results.extend(docs)



        fused = (
            self.rrf.fuse(
                all_results
            )
        )


        unique = (
            self.deduper.dedupe(
                fused
            )
        )
        

        reranked = await self.reranker.rerank(
            question,
            unique
        )


        reranked=reranked[:3]

        


        parent_map = await self.parent_expander.expand(
            reranked
        )

        parents = list(parent_map.values())

        

        # Merge child + parent
        final_documents = reranked + parents

        # Remove duplicates again
        final_documents = self.deduper.dedupe(
            final_documents
        )
        

        # Convert only here
        retrieved_documents= []
        

        for doc in final_documents:

            metadata = (
                ast.literal_eval(doc["metadata"])
                if isinstance(doc.get("metadata"), str)
                else doc.get("metadata", {})
            )

            retrieved_documents.append(

                RetrievedDocument(

                    id=doc["id"],

                    content=doc["content"],

                    document_id=doc.get("document_id"),

                    parent_id=doc.get("parent_id"),

                    source_file=metadata.get("source_file"),

                    page_number=metadata.get("page"),

                    metadata=metadata

                )

            )
            
        context = self.context_builder.build(
            retrieved_documents
        )

        return {
            "documents": retrieved_documents,
            "context": context["context"],
            "citation_map": context["citation_map"],
                }
      
            

        

        



