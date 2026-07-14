from io import BytesIO

from pypdf import PdfReader, PdfWriter


class PDFSplitter:
    """
    Splits a PDF into smaller PDFs.

    Can be reused with different split sizes.

    Example

    splitter.split(document)

    splitter.split(
        document,
        pages_per_split=1
    )
    """

    def __init__(
        self,
        pages_per_split: int = 5,
    ):
        self.pages_per_split = pages_per_split

    def split(
        self,
        document: bytes,
        pages_per_split: int | None = None,
    ):

        pages_per_split = (
            pages_per_split
            if pages_per_split is not None
            else self.pages_per_split
        )

        reader = PdfReader(
            BytesIO(document)
        )

        batches = []

        total_pages = len(reader.pages)

        for start in range(
            0,
            total_pages,
            pages_per_split,
        ):

            writer = PdfWriter()

            end = min(
                start + pages_per_split,
                total_pages,
            )

            for page_no in range(
                start,
                end,
            ):
                writer.add_page(
                    reader.pages[page_no]
                )

            output = BytesIO()

            writer.write(output)

            batches.append(
                {
                    "start_page": start + 1,
                    "end_page": end,
                    "content": output.getvalue(),
                }
            )

        return batches

    def page_count(
        self,
        document: bytes,
    ) -> int:

        reader = PdfReader(
            BytesIO(document)
        )

        return len(reader.pages)