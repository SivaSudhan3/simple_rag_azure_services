import asyncio

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError

from rag_interview.backend.document_processing.models import (
    AnalyzedDocument,
)

from rag_interview.core.config.config import (
    docsettings,
)


class DocumentIntelligenceService:

    def __init__(self):

        self.client = DocumentIntelligenceClient(

            docsettings.DOCUMENT_INTELLIGENT_ENDPOINT,

            AzureKeyCredential(
                docsettings.DOCUMENT_INTELLIGENT_KEY
            ),

            api_version="2024-11-30",
        )

    # ---------------------------------------------------
    # Analyze one PDF (sync)
    # ---------------------------------------------------

    def analyze(
        self,
        document: bytes,
    ):

        poller = self.client.begin_analyze_document(

            "prebuilt-layout",

            body=document,

            content_type="application/pdf",

            output_content_format="markdown",
        )

        return poller.result()

    # ---------------------------------------------------
    # Analyze one PDF (async wrapper)
    # ---------------------------------------------------

    async def _analyze_async(
        self,
        document: bytes,
        semaphore,
    ):

        async with semaphore:

            return await asyncio.to_thread(
                self.analyze,
                document,
            )

    # ---------------------------------------------------
    # Adaptive analysis
    # ---------------------------------------------------

    async def analyze_adaptive(
        self,
        document: bytes,
        document_context,
        splitter,
        semaphore,
    ):

        print(
            "Trying full PDF..."
        )

        try:

            result = await self._analyze_async(
                document,
                semaphore,
            )

            print(
                "Whole PDF analyzed successfully."
            )

            return [

                AnalyzedDocument(
                    context=document_context,
                    result=result,
                )

            ]

        except HttpResponseError as ex:

            if not self._is_image_limit(ex):
                raise

            print(
                "Whole PDF exceeded Azure image limit."
            )

        print(
            "Splitting into 5-page batches..."
        )

        analyzed_documents = []

        split_documents = splitter.split(

            document,

            pages_per_split=5,

        )

        tasks = [

            self._analyze_split(

                split,

                document_context,

                splitter,

                semaphore,

            )

            for split in split_documents

        ]

        results = await asyncio.gather(
            *tasks
        )

        for docs in results:

            analyzed_documents.extend(
                docs
            )

        return analyzed_documents

    # ---------------------------------------------------
    # Analyze one split
    # ---------------------------------------------------

    async def _analyze_split(
        self,
        split_document,
        document_context,
        splitter,
        semaphore,
    ):

        split_context = document_context.model_copy(

            update={

                "page_offset":
                    split_document["start_page"] - 1

            }

        )

        try:

            result = await self._analyze_async(

                split_document["content"],

                semaphore,

            )

            return [

                AnalyzedDocument(

                    context=split_context,

                    result=result,

                )

            ]

        except HttpResponseError as ex:

            if not self._is_image_limit(ex):
                raise

            print(

                f"Split "

                f"{split_document['start_page']}-"

                f"{split_document['end_page']} "

                f"still exceeds Azure image limit."

            )

        print(
            "Retrying page-by-page..."
        )

        single_pages = splitter.split(

            split_document["content"],

            pages_per_split=1,

        )

        tasks = [

            self._analyze_single_page(

                page,

                split_document,

                document_context,

                semaphore,

            )

            for page in single_pages

        ]

        results = await asyncio.gather(
            *tasks
        )

        analyzed = []

        for doc in results:
            analyzed.append(doc)

        return analyzed

    # ---------------------------------------------------
    # Analyze one page
    # ---------------------------------------------------

    async def _analyze_single_page(
        self,
        page_document,
        parent_split,
        document_context,
        semaphore,
    ):

        page_context = document_context.model_copy(

            update={

                "page_offset":

                    parent_split["start_page"]

                    + page_document["start_page"]

                    - 2

            }

        )

        result = await self._analyze_async(

            page_document["content"],

            semaphore,

        )

        return AnalyzedDocument(

            context=page_context,

            result=result,

        )

    # ---------------------------------------------------
    # Helpers
    # ---------------------------------------------------

    @staticmethod
    def _is_image_limit(
        ex: Exception,
    ) -> bool:

        if not isinstance(
            ex,
            HttpResponseError,
        ):
            return False

        text = str(ex)

        return (

            "InvalidContentLength" in text

            or

            "input image is too large" in text.lower()

        )