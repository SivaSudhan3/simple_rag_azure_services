from pypdf import PdfReader, PdfWriter
from io import BytesIO


class PDFSplitter:


    def __init__(
        self,
        pages_per_split=8
    ):

        self.pages_per_split = pages_per_split



    def split(
        self,
        document: bytes
    ):


        reader = PdfReader(
            BytesIO(document)
        )


        batches = []


        for start in range(
            0,
            len(reader.pages),
            self.pages_per_split
        ):


            writer = PdfWriter()


            end = min(
                start + self.pages_per_split,
                len(reader.pages)
            )


            for page_no in range(
                start,
                end
            ):

                writer.add_page(
                    reader.pages[page_no]
                )


            output = BytesIO()


            writer.write(
                output
            )


            batches.append(
                {
                    "start_page": start + 1,
                    "end_page": end,
                    "content": output.getvalue()
                }
            )


        return batches