from rag_interview.backend.prompts.generation_prompt import (
    GENERATION_PROMPT,
)

import tiktoken


class GenerationAgent:

    def __init__(
        self,
        llm_service,
    ):

        self.llm = llm_service

        self.encoding = tiktoken.get_encoding(
            "cl100k_base"
        )

    async def generate(
        self,
        state,
    ):

        messages = GENERATION_PROMPT.format_messages(

            question=state.question,

            context=state.context,

            chat_history=state.chat_history,

        )

        context_tokens = len(
            self.encoding.encode(state.context)
        )

        print(f"Context Tokens: {context_tokens}")

        # -----------------------------------------
        # Telemetry
        # -----------------------------------------

        state.telemetry.retrieval.context_characters = len(
            state.context
        )

        state.telemetry.retrieval.estimated_context_tokens = (
            context_tokens
        )

        response = await self.llm.generate(
            messages
        )

        state.answer = response

        return state

    async def stream_generate(
        self,
        state,
    ):

        messages = GENERATION_PROMPT.format_messages(

            question=state.question,

            context=state.context,

            chat_history=state.chat_history,

        )

        context_tokens = len(
            self.encoding.encode(state.context)
        )

        print(f"Context Tokens: {context_tokens}")

        # -----------------------------------------
        # Telemetry
        # -----------------------------------------

        state.telemetry.retrieval.context_characters = len(
            state.context
        )

        state.telemetry.retrieval.estimated_context_tokens = (
            context_tokens
        )

        answer = ""

        async for token in self.llm.stream(
            messages,
        ):

            answer += token

            yield token

        state.answer = answer