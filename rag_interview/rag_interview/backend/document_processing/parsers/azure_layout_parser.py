
from rag_interview.backend.document_processing.models import (
    DocumentBlock,
    BoundingBox,
)


class AzureLayoutParser:
    """
    Layout parser that reconstructs semantic document sections.

    Strategy
    --------
    1. Parse Document Intelligence paragraphs.
    2. Preserve paragraph roles.
    3. Merge paragraphs based on document structure rather than length.
    4. Stop merging when a new heading/title starts.
    5. Parse tables separately.
    """

    HEADING_ROLES = {
        "ParagraphRole.TITLE",
        "ParagraphRole.SECTION_HEADING",
    }

    IGNORE_ROLES = {
        "ParagraphRole.PAGE_HEADER",
        "ParagraphRole.PAGE_FOOTER",
        "ParagraphRole.PAGE_NUMBER",
    }

    def parse(self, analyzed_document):
        result = analyzed_document.result
        context = analyzed_document.context

        paragraph_blocks = self._parse_paragraphs(result, context)
        paragraph_blocks = self._merge_paragraphs(paragraph_blocks)

        table_blocks = self._parse_tables(result, context)

        blocks = paragraph_blocks + table_blocks
        blocks.sort(key=lambda b: (b.page_number, b.order))
        return blocks

    def _parse_paragraphs(self, result, context):
        blocks = []

        for index, para in enumerate(result.paragraphs or []):

            role = str(para.role) if para.role else None

            if role in self.IGNORE_ROLES:
                continue

            region = (
                para.bounding_regions[0]
                if para.bounding_regions
                else None
            )

            page_number = (
                region.page_number + context.page_offset
                if region
                else 0
            )

            block = DocumentBlock(
                document_id=context.document_id,
                content=para.content.strip(),
                content_type=(
                    "heading"
                    if role in self.HEADING_ROLES
                    else "text"
                ),
                page_number=page_number,
                order=(
                    para.spans[0].offset
                    if para.spans
                    else index
                ),
                bounding_box=(
                    BoundingBox(page_number=page_number)
                    if region
                    else None
                ),
                metadata={
                    "source_file": context.source_file,
                    "file_type": context.file_type,
                    "role": role,
                },
            )

            blocks.append(block)

        return blocks

    def _merge_paragraphs(self, blocks):
        """
        Merge paragraphs into semantic sections.

        Rules
        -----
        * A heading starts a new section.
        * Everything after a heading belongs to that section.
        * Stop when another heading is encountered.
        * Keep challenge/solution labels and bullets together.
        """

        if not blocks:
            return []

        merged = []
        current = None

        for block in blocks:

            if current is None:
                current = block
                continue

            current_role = current.metadata.get("role")
            block_role = block.metadata.get("role")

            # New title / section -> flush previous section
            if block_role in self.HEADING_ROLES:
                merged.append(current)
                current = block
                continue

            same_page = current.page_number == block.page_number

            should_merge = False

            if same_page:

                if current_role in self.HEADING_ROLES:
                    should_merge = True

                elif current.content.rstrip().endswith(":"):
                    should_merge = True

                elif block.content.lstrip().startswith(
                    ("1.", "2.", "3.", "4.", "5.", "-", "•")
                ):
                    should_merge = True

                elif (
                    current.content_type == "text"
                    and block.content_type == "text"
                ):
                    # Default: keep consecutive body paragraphs together
                    should_merge = True

            if should_merge:
                current.content += "\n\n" + block.content
                current.content_type = "text"
            else:
                merged.append(current)
                current = block

        if current is not None:
            merged.append(current)

        return merged

    def _parse_tables(self, result, context):
        output = []

        for index, table in enumerate(result.tables or []):

            rows = {}

            for cell in table.cells:
                rows.setdefault(cell.row_index, {})
                rows[cell.row_index][cell.column_index] = cell.content

            markdown = ""

            for row in rows.values():
                markdown += "|"
                for value in row.values():
                    markdown += value + "|"
                markdown += "\n"

            region = (
                table.bounding_regions[0]
                if table.bounding_regions
                else None
            )

            page_number = (
                region.page_number + context.page_offset
                if region
                else 0
            )

            output.append(
                DocumentBlock(
                    document_id=context.document_id,
                    content=markdown,
                    content_type="table",
                    page_number=page_number,
                    order=(
                        table.spans[0].offset
                        if table.spans
                        else index
                    ),
                    metadata={
                        "source_file": context.source_file,
                        "file_type": context.file_type,
                        "rows": table.row_count,
                        "columns": table.column_count,
                    },
                )
            )

        return output
