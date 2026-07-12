from rag_interview.agents.security.prompt_injection_agent import PromptInjectionAgent


from rag_interview.graph.graph_schema import GraphSchema



class Nodes:

    def __init__(
        self,
        content_agent,
        generation_agent,
        retrieval_agent,
        grounding_agent,
    ):
        self.content_agent = content_agent
        self.prompt_agent = PromptInjectionAgent()
        self.generation_agent = generation_agent
        self.retrieval_agent = retrieval_agent
        self.grounding_agent = grounding_agent

    def security_node(
        self,
        state: GraphSchema
    ):

        content_result = self.content_agent.analyze(
            state.question
        )

        attack_result = self.prompt_agent.scan(
            state.question
        )

        if (
            not content_result["safe"]
            or attack_result["attack"]
        ):

            state.is_safe = False

            state.blocked_reason = {
                "content": content_result,
                "prompt": attack_result
            }

            return state

        state.is_safe = True
        return state

    def blocked_node(
        self,
        state: GraphSchema
    ):

        state.answer = (
            "Request blocked by AI safety policy"
        )

        return state

    async def retrieval_node(
        self,
        state: GraphSchema
    ):

        

        result = await self.retrieval_agent.retrieve(
                 question=state.question,
                 chat_history=state.chat_history
            )

        state.documents= result.get(
                "documents",
                []
            )

        state.context = result.get(
                "context",
                ""
            )

        state.citation_map = result["citation_map"]

          

        return state

    async def generation_node(
        self,
        state: GraphSchema
    ):

        return await self.generation_agent.generate(
            state
        )
    async def grounding_node(
    self,
    state: GraphSchema
    ):

        return await self.grounding_agent.evaluate(
            state
        )
    async def generation_stream(self, state):
        async for token in self.generation_agent.stream_generate(state):
            yield token