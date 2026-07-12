
from rag_interview.backend.prompts.grounding_prompt import (
    GROUNDING_PROMPT
)
import json


class GroundingAgent:

    def __init__(
        self,
        llm
    ):

        self.llm = llm


    async def evaluate(
        self,
        state
    ):


        messages = GROUNDING_PROMPT.format_messages(

            question=state.question,

            context=state.context,

            answer=state.answer

        )


        response = await self.llm.generate(
            messages
        )


        result = json.loads(
            response
        )


        state.grounded_score = result.get(
            "grounded_score",
            0.0
        )


        state.relevance_score = result.get(
            "relevance_score",
            0.0
        )


        state.metrics["grounding_reason"] = result.get(
            "reason",
            ""
        )


        return state