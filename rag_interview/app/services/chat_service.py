from uuid import uuid4

from rag_interview.graph.graph_schema import GraphSchema

from app.schemas.schema import (
    ChatRequest,
    ChatResponse,
)

import json
import logging
import time
from uuid import uuid4

from app.security.models import CurrentUser
from rag_interview.services.conversation_services import ConversationService
from typing import AsyncGenerator
import json
logger = logging.getLogger(__name__)



class ChatService:

    def __init__(
        self,
        graph,
        nodes,
        conversation_service: ConversationService,
    ):
        self.graph = graph
        self.nodes = nodes
        self.conversation_service = conversation_service

    async def chat(
        self,
        request: ChatRequest,
        current_user: CurrentUser
        
    ) -> ChatResponse:

        # Reuse existing conversation or create a new one
        conversation_id = (
            request.conversation_id
            or str(uuid4())
        )

        # Load previous conversation history
        history = await self.conversation_service.get_history(
            conversation_id
        )

        history=history[-10:]

        # Build graph state
        state = GraphSchema(
            request_id=str(uuid4()),
            user_id=str(1),
            conversation_id=conversation_id,
            question=request.question,
            chat_history=history,
        )
        
            # Invoke LangGraph
        result = await self.graph.ainvoke(state)

        # Save user message
        await self.conversation_service.append_message(
            conversation_id=conversation_id,
            role="user",
            content=request.question,
        )

        # Save assistant response
        await self.conversation_service.append_message(
            conversation_id=conversation_id,
            role="assistant",
            content=result["answer"],
        )

        # Return response
        return ChatResponse(
            conversation_id=conversation_id,
            answer=result["answer"],
            grounded_score=result["grounded_score"],
            relevance_score=result["relevance_score"],
            request_id=result["request_id"],
        )


    async def stream_chat(
        self,
        request: ChatRequest,
        current_user: CurrentUser,
    ) -> AsyncGenerator[str, None]:

        # ============================================================
        # Request Start
        # ============================================================

        request_start = time.perf_counter()

        # Create / reuse conversation
        conversation_id = (
            request.conversation_id
            or str(uuid4())
        )

        if request.conversation_id is None:

            await self.conversation_service.create_conversation(
                conversation_id=conversation_id,
                title=request.question[:50],
            )

        # Load history
        history = await self.conversation_service.get_history(
            conversation_id
        )

        history = history[-10:]

        # Build graph state
        state = GraphSchema(
            request_id=str(uuid4()),
            user_id=current_user.id,
            conversation_id=conversation_id,
            question=request.question,
            chat_history=history,
        )

        # Notify client
        yield (
            "event: start\n"
            f"data: {json.dumps({
                'conversation_id': conversation_id,
                'request_id': state.request_id,
            })}\n\n"
        )

        # ============================================================
        # Security
        # ============================================================

        state = self.nodes.security_node(state)

        if not state.is_safe:

            state = self.nodes.blocked_node(state)

            yield (
                "event: blocked\n"
                f"data: {json.dumps({'message': state.answer})}\n\n"
            )

            yield (
                "event: done\n"
                f"data: {json.dumps({
                    'conversation_id': conversation_id,
                    'request_id': state.request_id,
                })}\n\n"
            )

            return

        # ============================================================
        # Retrieval
        # ============================================================

        retrieval_start = time.perf_counter()

        state = await self.nodes.retrieval_node(state)

        retrieval_end = time.perf_counter()

        logger.info(
            "Retrieval Stage : %.3f sec",
            retrieval_end - retrieval_start,
        )

        logger.info(
            "Elapsed Before Generation : %.3f sec",
            retrieval_end - request_start,
        )

        # ============================================================
        # Generation
        # ============================================================

        generation_start = time.perf_counter()

        first_token = True

        answer = ""

        async for token in self.nodes.generation_agent.stream_generate(
            state
        ):

            if first_token:

                first_token = False

                ttft = time.perf_counter() - request_start
                if hasattr(state, "telemetry"):
                    state.telemetry.timings.ttft_ms = ttft * 1000

                logger.info(
                    "TTFT (First Token) : %.3f sec",
                    ttft,
                )

                startup = time.perf_counter() - generation_start

                if hasattr(state, "telemetry"):
                    state.telemetry.timings.generation_startup_ms = startup * 1000

                logger.info(
                    "Generation Startup : %.3f sec",
                    startup,
                )

            answer += token

            yield (
                "event: token\n"
                f"data: {token}\n\n"
            )

        generation_end = time.perf_counter()

        generation_time = generation_end - generation_start

        if hasattr(state, "telemetry"):
            state.telemetry.timings.generation_ms = generation_time * 1000

        logger.info(
            "Generation Time : %.3f sec",
            generation_time,
        )

        logger.info(
            "Total Time Before Save : %.3f sec",
            generation_end - request_start,
        )

        state.answer = answer

        # ============================================================
        # Save Conversation
        # ============================================================

        await self.conversation_service.append_message(
            conversation_id,
            "user",
            request.question,
        )

        await self.conversation_service.append_message(
            conversation_id,
            "assistant",
            answer,
        )

        total_end = time.perf_counter()

        logger.info("=================================================")

        total_request = total_end - request_start

        if hasattr(state, "telemetry"):

            state.telemetry.timings.total_request_ms = (
                total_request * 1000
            )

            logger.info(
                "Telemetry Summary"
            )

            logger.info(
                state.telemetry.model_dump_json(
                    indent=2
                )
            )

        logger.info(
            "TOTAL REQUEST : %.3f sec",
            total_request,
        )

        logger.info("=================================================")

        yield (
            "event: done\n"
            f"data: {json.dumps({
                'conversation_id': conversation_id,
                'request_id': state.request_id,
                'grounded_score': state.grounded_score,
                'relevance_score': state.relevance_score,
                'citations': state.citation_map,
            })}\n\n"
        )