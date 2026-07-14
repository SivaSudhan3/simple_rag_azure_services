import asyncio
import logging

logger = logging.getLogger(__name__)


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

    async def expand(
        self,
        child_chunks,
    ):

        # ---------------------------------------
        # Collect unique parent IDs
        # ---------------------------------------

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
            logger.info("Parent Expansion : No parent IDs found")
            return {}

        logger.info(
            "Parent Expansion : Fetching %d parent(s)",
            len(parent_ids),
        )

        # ---------------------------------------
        # Fetch parents concurrently
        # ---------------------------------------

        parents = await asyncio.gather(
            *[
                self.search.get_document(parent_id)
                for parent_id in parent_ids
            ],
            return_exceptions=True,
        )

        # ---------------------------------------
        # Build parent map within token budget
        # ---------------------------------------

        parent_map = {}
        current_tokens = 0

        for parent in parents:

            if isinstance(parent, Exception):

                logger.warning(
                    "Failed to fetch parent document: %s",
                    parent,
                )

                continue

            estimated_tokens = len(
                parent["content"]
            ) // 4

            if (
                current_tokens
                + estimated_tokens
                > self.max_tokens
            ):

                logger.info(
                    "Skipping parent %s (token budget exceeded)",
                    parent["id"],
                )

                continue

            parent_map[parent["id"]] = parent

            current_tokens += estimated_tokens

        logger.info(
            "Parent Expansion : Expanded %d parent(s), Estimated Tokens=%d",
            len(parent_map),
            current_tokens,
        )

        return parent_map