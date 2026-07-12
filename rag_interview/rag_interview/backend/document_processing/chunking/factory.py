from .recursive_chunk import RecursiveChunker
from .parent_child import ParentChildChunker
from .semantic_chunking import SemanticDocumentChunker


class ChunkerFactory:


    @staticmethod
    def create(
        strategy,
        embeddings=None
    ):


        if strategy=="semantic":

            return SemanticDocumentChunker(
                embeddings
            )


        if strategy=="parent_child":

            return ParentChildChunker()



        return RecursiveChunker()