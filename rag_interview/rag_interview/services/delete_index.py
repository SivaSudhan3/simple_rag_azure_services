from rag_interview.core.dependencies import get_search_service


async def delete_documents() -> int:
    """
    Deletes every document from the Azure AI Search index.

    Returns:
        int: Number of documents deleted.
    """

    client = get_search_service().client

    
    results = await client.search(
            search_text="*",
            select=["id"],
        )

    documents = []

    async for doc in results:
            documents.append(
                {
                    "id": doc["id"]
                }
            )

    print(f"Found {len(documents)} documents")

    if documents:
            await client.delete_documents(documents=documents)
            print("Deleted successfully")

    return len(documents)
