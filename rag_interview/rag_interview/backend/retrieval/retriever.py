from rag_interview.graph.graph_schema import RetrievedDocument
import ast
import asyncio
import time
import logging

logger = logging.getLogger(__name__)


class Retriever:

    def __init__(
        self,
        expander,
        searcher,
        rrf,
        deduper,
        reranker,
        parent_expander,
        context_builder,
    ):
        self.expander = expander
        self.searcher = searcher
        self.rrf = rrf
        self.deduper = deduper
        self.reranker = reranker
        self.parent_expander = parent_expander
        self.context_builder = context_builder

    async def retrieve(
        self,
        question,
        chat_history: list[dict] | None = None,
        telemetry=None,
    ):

        overall_start = time.perf_counter()

        logger.info("=" * 80)
        logger.info("RETRIEVAL PIPELINE START")
        logger.info("Question: %s", question)
        logger.info("=" * 80)

        # -------------------------------------------------------
        # Query Expansion
        # -------------------------------------------------------

        t = time.perf_counter()

        # queries = await self.expander.expand(
        #     question=question,
        #     chat_history=chat_history
        # )

        queries = [question]

        logger.info(
            "Query Expansion : %.3f sec | Queries=%d",
            time.perf_counter() - t,
            len(queries),
        )

        print("\n" + "=" * 100)
        print("QUERY EXPANSION")
        print("=" * 100)
        for i, q in enumerate(queries, 1):
            print(f"{i}. {q}")

        # -------------------------------------------------------
        # Search
        # -------------------------------------------------------

        t = time.perf_counter()

        tasks = [
            self.searcher.search(query, telemetry=telemetry)
            for query in queries
        ]

        results = await asyncio.gather(*tasks)

        all_results = []

        print("\n" + "=" * 100)
        print("HYBRID SEARCH RESULTS")
        print("=" * 100)

        for q_idx, docs in enumerate(results, 1):

            print(f"\nQUERY {q_idx}")

            print("\nVECTOR RESULTS")
            for i, doc in enumerate(docs[0], 1):
                print(f"\n[{i}]")
                print("ID:", doc.get("id"))
                print("Score:", doc.get("@search.score"))
                print("Parent:", doc.get("parent_id"))
                print("Metadata:", doc.get("metadata"))
                print("Content:\n", doc.get("content", "")[:500])

            print("\nLEXICAL RESULTS")
            for i, doc in enumerate(docs[1], 1):
                print(f"\n[{i}]")
                print("ID:", doc.get("id"))
                print("Score:", doc.get("@search.score"))
                print("Parent:", doc.get("parent_id"))
                print("Metadata:", doc.get("metadata"))
                print("Content:\n", doc.get("content", "")[:500])

            all_results.extend(docs)

        logger.info(
            "Hybrid Search  : %.3f sec | Results=%d",
            time.perf_counter() - t,
            len(all_results),
        )

        # -------------------------------------------------------
        # RRF
        # -------------------------------------------------------

        t = time.perf_counter()

        fused = self.rrf.fuse(all_results)

        print("\n" + "=" * 100)
        print("RRF OUTPUT")
        print("=" * 100)

        for i, doc in enumerate(fused, 1):
            print(f"\n[{i}]")
            print("ID:", doc.get("id"))
            print("Score:", doc.get("@search.score"))
            print("Content:\n", doc.get("content", "")[:500])

        logger.info(
            "RRF            : %.3f sec | Results=%d",
            time.perf_counter() - t,
            len(fused),
        )

        # -------------------------------------------------------
        # Dedupe
        # -------------------------------------------------------

        t = time.perf_counter()

        unique = self.deduper.dedupe(fused)

        print("\n" + "=" * 100)
        print("DEDUPED OUTPUT")
        print("=" * 100)

        for i, doc in enumerate(unique, 1):
            print(f"\n[{i}]")
            print(doc.get("content", "")[:500])

        logger.info(
            "Dedupe         : %.3f sec | Results=%d",
            time.perf_counter() - t,
            len(unique),
        )

        # -------------------------------------------------------
        # Azure Semantic Reranker
        # -------------------------------------------------------

        t = time.perf_counter()

        reranked = await self.reranker.rerank(
            question,
            unique,
        )

        print("\n" + "=" * 100)
        print("SEMANTIC RERANKER OUTPUT")
        print("=" * 100)

        for i, doc in enumerate(reranked, 1):
            print(f"\n[{i}]")
            print(doc.get("content", "")[:500])

        semantic_time = time.perf_counter() - t

        if telemetry:
            telemetry.timings.semantic_ranking_ms = semantic_time * 1000
            telemetry.retrieval.semantic_results = len(reranked)

        logger.info(
            "Semantic Rank  : %.3f sec | Results=%d",
            semantic_time,
            len(reranked),
        )

        reranked = reranked[:3]

        # -------------------------------------------------------
        # Parent Expansion
        # -------------------------------------------------------

        t = time.perf_counter()

        parent_map = await self.parent_expander.expand(
            reranked
        )

        print("\n" + "=" * 100)
        print("PARENT DOCUMENTS")
        print("=" * 100)

        for i, doc in enumerate(parent_map.values(), 1):
            print(f"\n[{i}]")
            print(doc.get("content", "")[:500])

        parent_time = time.perf_counter() - t

        if telemetry:
            telemetry.timings.parent_expansion_ms = parent_time * 1000

        logger.info(
            "Parent Expand  : %.3f sec | Parents=%d",
            parent_time,
            len(parent_map),
        )

        parents = list(parent_map.values())

        # -------------------------------------------------------
        # Merge
        # -------------------------------------------------------

        t = time.perf_counter()

        final_documents = reranked + parents

        final_documents = self.deduper.dedupe(
            final_documents
        )

        print("\n" + "=" * 100)
        print("FINAL DOCUMENTS")
        print("=" * 100)

        for i, doc in enumerate(final_documents, 1):
            print(f"\n[{i}]")
            print(doc.get("content", "")[:500])

        logger.info(
            "Merge+Dedupe   : %.3f sec | Results=%d",
            time.perf_counter() - t,
            len(final_documents),
        )

        t = time.perf_counter()

        retrieved_documents = []

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
                    metadata=metadata,
                )
            )

        logger.info(
            "DTO Convert    : %.3f sec",
            time.perf_counter() - t,
        )

        t = time.perf_counter()

        context = self.context_builder.build(
            retrieved_documents
        )

        print("\n" + "=" * 100)
        print("FINAL CONTEXT SENT TO LLM")
        print("=" * 100)
        print(context["context"])

        context_time = time.perf_counter() - t

        if telemetry:
            telemetry.timings.context_build_ms = context_time * 1000
            telemetry.timings.retrieval_total_ms = (
                time.perf_counter() - overall_start
            ) * 1000
            telemetry.retrieval.final_documents = len(retrieved_documents)
            telemetry.retrieval.context_characters = len(context["context"])
            telemetry.retrieval.estimated_context_tokens = (
                len(context["context"]) // 4
            )

        logger.info(
            "Context Build  : %.3f sec",
            context_time,
        )

        logger.info("=" * 80)
        logger.info(
            "TOTAL RETRIEVAL: %.3f sec",
            time.perf_counter() - overall_start,
        )
        logger.info("=" * 80)

        return {
            "documents": retrieved_documents,
            "context": context["context"],
            "citation_map": context["citation_map"],
        }
