from rag_interview.core.dependencies import get_retriever
import asyncio


async def main():

    retriever = get_retriever()

    results = await retriever.retrieve(
        "What is Reconfigurable Intelligent Surface?"
    )

    print("TOTAL RESULTS:", len(results))

    

    documents = results["documents"]

    context = results["context"]

    print("=" * 80)
    print("CONTEXT SENT TO LLM")
    print("=" * 80)

    print(context)

    print("\nRetrieved Documents:", len(documents))

    for i, doc in enumerate(documents, start=1):

        print(f"\nSource {i}")

        print(f"ID: {doc.id}")

        print(f"File: {doc.source_file}")

        print(f"Page: {doc.page_number}")

        print(doc.content[:300])
if __name__ == "__main__":
    asyncio.run(main())