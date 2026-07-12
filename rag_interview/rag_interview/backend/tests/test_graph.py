import asyncio
import uuid

from rag_interview.graph.workflow import app_graph
from rag_interview.graph.graph_schema import GraphSchema


async def main():

    state = GraphSchema(

        request_id=str(uuid.uuid4()),

        user_id="test_user",

        question="What is Reconfigurable Intelligent Surface?"

    )

    result = await app_graph.ainvoke(state)

    print("=" * 80)
    print("QUESTION")
    print("=" * 80)
    print(result["question"])

    print("\n")

    print("=" * 80)
    print("ANSWER")
    print("=" * 80)
    print(result["answer"])

    print("\n")

    print("=" * 80)
    print("SAFE")
    print("=" * 80)
    print(result["is_safe"])

    print("\n")

    print("=" * 80)
    print("GROUNDING SCORE")
    print("=" * 80)
    print(result["grounded_score"])

    print("\n")

    print("=" * 80)
    print("RELEVANCE SCORE")
    print("=" * 80)
    print(result["relevance_score"])

    print("\n")

    print("=" * 80)
    print("CONTEXT")
    print("=" * 80)
    print(result["context"])

    print("\n")

    print("=" * 80)
    print("DOCUMENTS")
    print("=" * 80)

    documents = result["documents"]

    print("Retrieved:", len(documents))

    for i, doc in enumerate(documents, start=1):

        print(f"\nSource {i}")

        print("ID:", doc.id)

        print("File:", doc.source_file)

        print("Page:", doc.page_number)

        print(doc.content[:300])


if __name__ == "__main__":

    asyncio.run(main())