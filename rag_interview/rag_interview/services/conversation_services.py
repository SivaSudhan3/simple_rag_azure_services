from __future__ import annotations

import json
from datetime import datetime

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

    async def create_conversation(
        self,
        conversation_id: str,
        title: str,
    ) -> None:

        key = self._get_key(conversation_id)

        if await self.redis.exists(key):
            return

        conversation = {
            "id": conversation_id,
            "title": title,
            "updated_at": datetime.utcnow().isoformat(),
            "messages": [],
        }

        await self.redis.set(
            key,
            json.dumps(conversation),
            ex=86400,
        )

    async def get_conversation(
        self,
        conversation_id: str,
    ) -> dict | None:

        data = await self.redis.get(
            self._get_key(conversation_id)
        )

        if not data:
            return None

        return json.loads(data)

    async def get_history(
        self,
        conversation_id: str,
    ) -> list[dict]:

        conversation = await self.get_conversation(
            conversation_id
        )

        if not conversation:
            return []

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

        conversation = await self.get_conversation(
            conversation_id
        )

        if conversation is None:

            conversation = {
                "id": conversation_id,
                "title": content[:50],
                "updated_at": datetime.utcnow().isoformat(),
                "messages": [],
            }

        conversation["messages"].append(
            {
                "role": role,
                "content": content,
            }
        )

        conversation["updated_at"] = datetime.utcnow().isoformat()

        await self.redis.set(
            self._get_key(conversation_id),
            json.dumps(conversation),
            ex=86400,
        )

    async def list_conversations(
        self,
    ) -> list[dict]:

        keys = await self.redis.keys("conversation:*")

        conversations = []

        for key in keys:

            data = await self.redis.get(key)

            if not data:
                continue

            conversation = json.loads(data)

            conversations.append(
                {
                    "id": conversation["id"],
                    "title": conversation["title"],
                    "updated_at": conversation["updated_at"],
                }
            )

        conversations.sort(
            key=lambda x: x["updated_at"],
            reverse=True,
        )

        return conversations

    async def delete(
        self,
        conversation_id: str,
    ) -> None:

        await self.redis.delete(
            self._get_key(conversation_id)
        )
    async def delete_all(self) -> None:
        """
        Delete all keys in the current Redis database.
        """
        await self.redis.flushdb()