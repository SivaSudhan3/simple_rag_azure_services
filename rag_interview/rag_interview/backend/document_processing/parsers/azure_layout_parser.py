from rag_interview.backend.document_processing.models import (
    DocumentBlock,
    BoundingBox
)



class AzureLayoutParser:


    def parse(
        self,
        analyzed_document,
        
    ):
        result=analyzed_document.result
        context=analyzed_document.context


        blocks = []


        blocks.extend(
            self._parse_paragraphs(result,context)
        )


        blocks.extend(
            self._parse_tables(result,context)
        )


        # restore document order

        blocks.sort(
            key=lambda x:
            (
                x.page_number,
                x.order
            )
        )


        return blocks
    def _parse_paragraphs(
        self,
        result,
        context
    ):


        output = []


        for index, para in enumerate(
            result.paragraphs or []
        ):


            region = (
                para.bounding_regions[0]
                if para.bounding_regions
                else None
            )


            block = DocumentBlock(

                document_id=context.document_id,

                content=
                para.content,


                content_type=
                "text",


                page_number=
                region.page_number
                if region else 0,


                order=
                index,


                bounding_box=
                BoundingBox(

                    page_number=
                    region.page_number

                )
                if region else None,
                metadata={
                "source_file":
                    context.source_file,


                "file_type":
                    context.file_type
            }
                        

            )


            output.append(block)


        return output
    def _parse_tables(
        self,
        result,
        context
    ):


        output=[]


        for index, table in enumerate(
            result.tables or []
        ):


            rows={}


            for cell in table.cells:


                rows.setdefault(
                    cell.row_index,
                    {}
                )


                rows[cell.row_index][
                    cell.column_index
                ] = cell.content



            markdown = ""


            for row in rows.values():


                markdown += "|"


                for value in row.values():


                    markdown += (
                        value + "|"
                    )


                markdown += "\n"



            region = (
                table.bounding_regions[0]
                if table.bounding_regions
                else None
            )


            output.append(

                DocumentBlock(

                    document_id=context.document_id,

                    content=markdown,


                    content_type="table",


                    page_number=
                    region.page_number
                    if region else 0,


                    order=index,


                    metadata={

                          
                    "source_file":
                        context.source_file,


                    "file_type":
                        context.file_type,
                

                    

                      "rows":
                      table.row_count,


                      "columns":
                      table.column_count

                    }

                )

            )


        return output