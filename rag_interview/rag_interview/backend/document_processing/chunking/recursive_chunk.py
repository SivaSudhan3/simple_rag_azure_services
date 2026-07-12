from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)


from rag_interview.backend.document_processing.models import Chunk
from .base import ChunkingStrategy



class RecursiveChunker(
    ChunkingStrategy
):


    def __init__(self):


        self.splitter = (
            RecursiveCharacterTextSplitter(

                chunk_size=1000,

                chunk_overlap=200

            )
        )



    def create_chunks(
        self,
        blocks
    ):


        chunks=[]


        for block in blocks:


            # never split tables

            if block.content_type=="table":


                chunks.append(

                    Chunk(

                        content=block.content,


                        embedding_content=
                        block.content,


                        chunk_type="table",


                        metadata={
                            **block.metadata,

                            "page":
                            block.page_number,

                            "content_type":
                            "table"
                        }

                    )

                )


                continue



            parts = (
                self.splitter
                .split_text(
                    block.content
                )
            )


            for part in parts:


                chunks.append(

                    Chunk(

                        content=part,

                        embedding_content=part,

                        chunk_type=
                        "recursive",


                        metadata={

                            **block.metadata,

                            "page":
                            block.page_number,

                            "content_type":
                            block.content_type

                        }

                    )

                )


        return self._link_chunks(
            chunks
        )



    def _link_chunks(
        self,
        chunks
    ):


        for i,chunk in enumerate(chunks):


            chunk.metadata[
                "previous_chunk_id"
            ] = (
                chunks[i-1].id
                if i>0
                else None
            )


            chunk.metadata[
                "next_chunk_id"
            ] = (
                chunks[i+1].id
                if i<len(chunks)-1
                else None
            )


            chunk.metadata[
                "chunk_index"
            ] = i


        return chunks