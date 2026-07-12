from rag_interview.core.dependencies import get_retriever

retriever = get_retriever()


from rag_interview.graph.graph_schema import GraphSchema


async def retrieval_node(
    self,
    state: GraphSchema
):

    result = await self.retrieval_agent.retrieve(
        state.question
    )

    state.documents = result["documents"]

    state.context = result["context"]

    return state