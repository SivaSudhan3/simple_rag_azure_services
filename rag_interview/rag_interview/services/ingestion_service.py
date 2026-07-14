from pathlib import Path
import asyncio
import time

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
from rag_interview.core.telemetry.telemetry_models import TelemetryMetrics


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
    
    

 
   
    async def ingest(
        self,
        job_id: str,
        blob_name: str,
        original_filename: str,
        telemetry: TelemetryMetrics | None = None,
        
    ) -> None:

        print(f"Starting ingestion: {job_id}")

        overall_start = time.perf_counter()

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

        t = time.perf_counter()
        

        analyzed_documents = await self.document_intelligence.analyze_adaptive(
            document=document,
            document_context=document_context,
            splitter=self.splitter,
            semaphore=self.semaphore,
        )




        if telemetry:
            telemetry.timings.document_analysis_ms = (time.perf_counter()-t)*1000
            telemetry.ingestion.documents_processed = 1
            telemetry.ingestion.pages_processed = (self.splitter.page_count(document))
                    

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

        print("=" * 120)
        print("LAYOUT BLOCKS")
        print("=" * 120)

        for i, block in enumerate(blocks):

            print(f"\nBLOCK {i+1}")
            print(f"Page        : {block.page_number}")
            print(f"Type        : {block.content_type}")
            print(f"Characters  : {len(block.content)}")

            print("-" * 80)
            print(block.content)
            print("-" * 80)
        
                

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

        t = time.perf_counter()

        chunks = chunker.create_chunks(
            enriched_blocks
        )

        if telemetry:
            telemetry.timings.chunking_ms = (time.perf_counter()-t)*1000
            telemetry.ingestion.chunks_created = len(chunks)

        print(
            f"Created {len(chunks)} chunks"
        )

        # ---------------------------------------------------
        # Embeddings
        # ---------------------------------------------------

        t = time.perf_counter()

        valid_chunks, vectors = await self.embedding_service.embed_documents(
            chunks
        )

        if telemetry:
            telemetry.timings.embedding_generation_ms = (time.perf_counter()-t)*1000
            telemetry.ingestion.embeddings_generated = len(valid_chunks)

        print("Embeddings generated")

        # ---------------------------------------------------
        # Azure AI Search
        # ---------------------------------------------------

        t = time.perf_counter()

        await self.search_service.index_chunks(
            chunks,
            valid_chunks,
            vectors
        )

        if telemetry:
            telemetry.timings.indexing_ms = (time.perf_counter()-t)*1000
            telemetry.timings.ingestion_total_ms = (time.perf_counter()-overall_start)*1000
            telemetry.ingestion.vectors_indexed = len(valid_chunks)

        print(
            f"Ingestion completed successfully "
            f"for job {job_id}"
        )