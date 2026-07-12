from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)


from ..models import Chunk



class ParentChildChunker:


    def __init__(self):


        self.child_splitter = (
            RecursiveCharacterTextSplitter(

                chunk_size=400,

                chunk_overlap=80

            )
        )



    def create_chunks(
        self,
        blocks
    ):


        final_chunks=[]


        for block in blocks:


            parent = Chunk(

                document_id=block.document_id,

                content=
                block.content,


                embedding_content=
                "",


                chunk_type=
                "parent",


                metadata={

                    **block.metadata,

                    "page":
                    block.page_number

                }

            )


            final_chunks.append(
                parent
            )



            children = (

                self.child_splitter
                .split_text(
                    block.content
                )

            )



            for child in children:


                final_chunks.append(

                    Chunk(

                        document_id=block.document_id,

                        content=child,


                        embedding_content=child,


                        chunk_type=
                        "child",


                        parent_id=
                        parent.id,


                        metadata={

                          **block.metadata,

                          "parent_id":
                          parent.id,

                          "page": block.page_number

                        }

                    )

                )


        return final_chunks