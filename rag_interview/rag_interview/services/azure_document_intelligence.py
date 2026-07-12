from azure.ai.documentintelligence  import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from rag_interview.core.config.config import docsettings
class DocumentIntelligenceService:
    def __init__(self):
        self.client=DocumentIntelligenceClient(
            docsettings.DOCUMENT_INTELLIGENT_ENDPOINT,
            AzureKeyCredential(docsettings.DOCUMENT_INTELLIGENT_KEY)
        )
    

    def analyze(
        self,
        document
    ):


        poller = (
            self.client
            .begin_analyze_document(

                "prebuilt-layout",

                body=document,
                content_type="application/pdf"

            )
        )


        return (
            poller.result()
        )
