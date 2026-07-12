import asyncio

from rag_interview.services.azure_document_intelligence import (
    DocumentIntelligenceService
)

from rag_interview.backend.document_processing.parsers.azure_layout_parser import (
    AzureLayoutParser
)

from rag_interview.backend.document_processing.enrichment.enricher import (
    ContextEnricher
)

from rag_interview.backend.document_processing.chunking.factory import (
    ChunkerFactory
)
from rag_interview.backend.document_processing.splitter.page_splitter import (
    PDFSplitter
)
from rag_interview.services.embedding import EmbeddingService
from rag_interview.services.azure_ai_search import AzureSearchService
from pathlib import Path
from rag_interview.backend.document_processing.models import (
    DocumentContext,
    AnalyzedDocument
)


async def test_pipeline():


    file_path = Path(
    "/mnt/c/Users/Administrator/Downloads/rag_interview (2)/rag_interview/rag_interview/backend/sample_docs/Emerging_Technologies_in_Intelligent_Metasurfaces_Shaping_the_Future_of_Wireless_Communications.pdf"
    )


   
    


    document_context = DocumentContext(

        source_file=file_path.name,

        file_type=file_path.suffix

    )


    # 1. Azure extraction

    extractor = (
        DocumentIntelligenceService()
    )


    with open(file_path,"rb") as f:
        document=f.read()
        splitter = PDFSplitter(
        pages_per_split=5
    )


    documents = splitter.split(
        document
    )


    results = []


    for doc in documents:


        print(
            "Processing pages:",
            doc["start_page"],
            "-",
            doc["end_page"]
        )


        result =  extractor.analyze(
            doc["content"]
        )

        analyzed_document = AnalyzedDocument(

        context=document_context,

        result=result)


        results.append(
            analyzed_document
        )
    

    


    print(
        "Document Intelligence completed"
    )


    # 2. Parse layout

    parser = AzureLayoutParser()

    blocks = []


    for result in results:


        blocks.extend(
            parser.parse(
                result
            )
        )


  


    print(
        "\nBLOCKS"
    )

    for block in blocks:


        print(
            block.content_type,
            block.page_number,
            block.content[:100]
        )



    # 3. Context enrichment


    enricher = ContextEnricher()


    enriched_blocks = (
        enricher.enrich(
            blocks
        )
    )


    print(
        "\nENRICHED"
    )


    for block in enriched_blocks:


        if block.content_type=="table":


            print(
                block.content
            )


    # 4. Chunking


    chunker = (
        ChunkerFactory.create(
            "parent_child"
        )
    )


    chunks = (
        chunker
        .create_chunks(
            enriched_blocks
        )
    )


    print(
        "\nCHUNKS CREATED:",
        len(chunks)
    )

    embedding_service=EmbeddingService()
    embeddings=await embedding_service.embed_documents(chunks)
    print("embedding_created")
    search_service=AzureSearchService()
    knowledge_base=await search_service.index_chunks(chunks,embeddings)
    print("KB created Moneyy")



asyncio.run(
    test_pipeline()
)