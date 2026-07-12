from rag_interview.services.azure_document_intelligence import (
    DocumentIntelligenceService
)


from rag_interview.backend.document_processing.parsers.azure_layout_parser import (
    AzureLayoutParser
)


from rag_interview.backend.document_processing.enrichment.enricher import (
    ContextEnricher
)



class DocumentAgent:


    def __init__(self):


        self.extractor = (
            DocumentIntelligenceService()
        )


        self.parser = (
            AzureLayoutParser()
        )


        self.enricher = (
            ContextEnricher()
        )



    async def process(
        self,
        file
    ):


        result = (
            await self.extractor
            .analyze(file)
        )


        blocks = (
            self.parser
            .parse(result)
        )


        enriched_blocks = (
            self.enricher
            .enrich(blocks)
        )


        return enriched_blocks