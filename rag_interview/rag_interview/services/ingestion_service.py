from pathlib import Path
import asyncio

from rag_interview.backend.document_processing.models import (
    DocumentContext,
    AnalyzedDocument,
)

from rag_interview.backend.document_processing.splitter.page_splitter import (
    PDFSplitter,
)

from rag_interview.backend.document_processing.parsers.azure_layout_parser import (
    AzureLayoutParser,
)

from rag_interview.backend.document_processing.enrichment.enricher import (
    ContextEnricher,
)

from rag_interview.backend.document_processing.chunking.factory import (
    ChunkerFactory,
)


class IngestionService:
    """
    Orchestrates the complete document ingestion pipeline.

    Blob Storage
            ↓
    Document Intelligence
            ↓
    Layout Parser
            ↓
    Context Enrichment
            ↓
    Chunking
            ↓
    Embeddings
            ↓
    Azure AI Search
    """

    def __init__(
        self,
        blob_storage,
        document_intelligence,
        embedding_service,
        search_service,
    ):

        self.blob_storage = blob_storage

        self.document_intelligence = document_intelligence

        self.embedding_service = embedding_service

        self.search_service = search_service

        # Lightweight components
        self.splitter = PDFSplitter(
            pages_per_split=5
        )

        self.parser = AzureLayoutParser()

        self.enricher = ContextEnricher()
        self.semaphore = asyncio.Semaphore(3)
    

    async def _analyze_split(self, split_document, document_context):
        
        async with self.semaphore:
            result = await asyncio.to_thread(
                self.document_intelligence.analyze,
                split_document["content"]
            )

        return AnalyzedDocument(
            context=document_context,
            result=result,
        )
   
    async def ingest(
        self,
        job_id: str,
        blob_name: str,
        original_filename: str,
    ) -> None:

        print(f"Starting ingestion: {job_id}")

        # ---------------------------------------------------
        # Download document from Azure Blob Storage
        # ---------------------------------------------------

        document =  self.blob_storage.download(
            blob_name
        )

        blob_path = Path(blob_name)

        document_context = DocumentContext(
            source_file=original_filename,
            file_type=Path(original_filename).suffix,
            
        )

       

        # ---------------------------------------------------
        # Split PDF
        # ---------------------------------------------------

        split_documents = self.splitter.split(
            document
        )


        tasks = [
            self._analyze_split(
                split_document,
                document_context,
            )
            for split_document in split_documents
        ]

        analyzed_documents = await asyncio.gather(*tasks)



        print("Document Intelligence completed")

        # ---------------------------------------------------
        # Layout Parsing
        # ---------------------------------------------------

        blocks = []

        for analyzed_document in analyzed_documents:

            blocks.extend(

                self.parser.parse(
                    analyzed_document
                )

            )

        print(
            f"Parsed {len(blocks)} layout blocks"
        )

        print(blocks[0])

        # ---------------------------------------------------
        # Context Enrichment
        # ---------------------------------------------------

        enriched_blocks = self.enricher.enrich(
            blocks
        )

        print(
            f"Enriched {len(enriched_blocks)} blocks"
        )

        # ---------------------------------------------------
        # Chunking
        # ---------------------------------------------------

        chunker = ChunkerFactory.create(
            "parent_child"
        )

        chunks = chunker.create_chunks(
            enriched_blocks
        )

        print(
            f"Created {len(chunks)} chunks"
        )

        # ---------------------------------------------------
        # Embeddings
        # ---------------------------------------------------

        valid_chunks, vectors = await self.embedding_service.embed_documents(
            chunks
        )

        print("Embeddings generated")

        # ---------------------------------------------------
        # Azure AI Search
        # ---------------------------------------------------

        await self.search_service.index_chunks(
            valid_chunks,
            vectors
        )

        print(
            f"Ingestion completed successfully "
            f"for job {job_id}"
        )