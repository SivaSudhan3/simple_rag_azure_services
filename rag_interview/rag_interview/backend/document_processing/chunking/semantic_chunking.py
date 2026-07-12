from langchain_experimental.text_splitter import (
    SemanticChunker
)


from ..models import Chunk



class SemanticDocumentChunker:


    def __init__(
        self,
        embeddings
    ):


        self.splitter = SemanticChunker(

            embeddings

        )



    def create_chunks(
        self,
        blocks
    ):


        chunks=[]


        for block in blocks:


            docs = (

                self.splitter
                .create_documents(

                    [
                        block.content
                    ]

                )

            )


            for doc in docs:


                chunks.append(

                    Chunk(

                        content=
                        doc.page_content,


                        embedding_content=
                        doc.page_content,


                        chunk_type=
                        "semantic",


                        metadata={

                            **block.metadata,


                            "page":
                            block.page_number

                        }

                    )

                )


        return chunks