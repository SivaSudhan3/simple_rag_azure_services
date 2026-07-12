from uuid import uuid4

from rag_interview.graph.graph_schema import GraphSchema

from app.schemas.schema import (
    ChatRequest,
    ChatResponse,
)

from app.security.models import CurrentUser
from rag_interview.services.conversation_services import ConversationService
from typing import AsyncGenerator
import json



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
            current_user: CurrentUser
        ) -> AsyncGenerator[str, None]:

            # Create / reuse conversation
            conversation_id = (
                request.conversation_id
                or str(uuid4())
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

            # Notify client that streaming has started
            yield (
                "event: start\n"
                f"data: {json.dumps({
                    'conversation_id': conversation_id,
                    'request_id': state.request_id,
                })}\n\n"
            )

            # -------------------------
            # Security
            # -------------------------
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

            # -------------------------
            # Retrieval
            # -------------------------
            state = await self.nodes.retrieval_node(
                state
            )

            # -------------------------
            # Generation (Streaming)
            # -------------------------
            answer = ""

            async for token in self.nodes.generation_agent.stream_generate(
                state
            ):

                answer += token

                yield (
                    "event: token\n"
                    f"data: {token}\n\n"
                )

            state.answer = answer

            # -------------------------
            # Grounding
            # -------------------------
           

            # -------------------------
            # Save Conversation
            # -------------------------
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

            # -------------------------
            # Stream Complete
            # -------------------------
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