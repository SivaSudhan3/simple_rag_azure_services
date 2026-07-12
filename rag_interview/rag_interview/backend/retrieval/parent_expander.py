import asyncio


class ParentExpander:

    def __init__(
        self,
        search_service,
        max_parents=3,
        max_tokens=6000,
    ):
        self.search = search_service
        self.max_parents = max_parents
        self.max_tokens = max_tokens

    async def expand(self, child_chunks):

        parent_ids = []
        seen = set()

        for chunk in child_chunks:

            parent_id = chunk.get("parent_id")

            if not parent_id:
                continue

            if parent_id in seen:
                continue

            seen.add(parent_id)
            parent_ids.append(parent_id)

            if len(parent_ids) >= self.max_parents:
                break

        if not parent_ids:
            return {}

        parents = await asyncio.gather(
            *[
                self.search.get_document(parent_id)
                for parent_id in parent_ids
            ]
        )

        parent_map = {}

        current_tokens = 0

        for parent in parents:

            estimated_tokens = len(parent["content"]) // 4

            if current_tokens + estimated_tokens > self.max_tokens:
                continue

            parent_map[parent["id"]] = parent
            current_tokens += estimated_tokens

        return parent_map