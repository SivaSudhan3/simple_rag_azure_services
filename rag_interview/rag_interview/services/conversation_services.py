from __future__ import annotations

import json

from redis.asyncio import Redis


class ConversationService:

    def __init__(
        self,
        redis: Redis,
    ):
        self.redis = redis

    def _get_key(
        self,
        conversation_id: str,
    ) -> str:
        return f"conversation:{conversation_id}"

    async def get_history(
        self,
        conversation_id: str,
    ) -> list[dict]:

        data = await self.redis.get(
            self._get_key(conversation_id)
        )

        if not data:
            return []

        conversation = json.loads(data)

        return conversation.get(
            "messages",
            [],
        )

    async def append_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
    ) -> None:

        history = await self.get_history(
            conversation_id
        )

        history.append(
            {
                "role": role,
                "content": content,
            }
        )

        await self.redis.set(
            self._get_key(conversation_id),
            json.dumps(
                {
                    "messages": history,
                }
            ),
            ex=86400,
        )

    async def delete(
        self,
        conversation_id: str,
    ) -> None:

        await self.redis.delete(
            self._get_key(conversation_id)
        )