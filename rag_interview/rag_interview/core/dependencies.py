from rag_interview.services.embedding import EmbeddingService
from rag_interview.services.azure_ai_search import AzureSearchService
from rag_interview.services.azure_content_safety import ContentSafetyAgent
from rag_interview.services.llm import get_llm_service

from rag_interview.agents.generation.generation import GenerationAgent

from rag_interview.backend.retrieval.query_expander import QueryExpander
from rag_interview.backend.retrieval.hybrid_search import HybridSearcher
from rag_interview.backend.retrieval.rrf import ReciprocalRankFusion
from rag_interview.backend.retrieval.deduplicator import Deduplicator
from rag_interview.backend.retrieval.retriever import Retriever
from rag_interview.backend.retrieval.parent_expander import ParentExpander
from rag_interview.backend.retrieval.reranker import Reranker
from rag_interview.backend.retrieval.context_builder import ContextBuilder


from rag_interview.agents.security.grounding_agent import GroundingAgent
from rag_interview.services.azure_blob import BlobStorageService
from rag_interview.services.azure_document_intelligence import DocumentIntelligenceService




from app.services.chat_service import ChatService
from app.services.document_service import DocumentService
from rag_interview.services.ingestion_service import IngestionService

from redis.asyncio import Redis
from rag_interview.core.config.config import celery_settings
from rag_interview.services.conversation_services import ConversationService

from rag_interview.graph.nodes.nodes import Nodes



_redis = Redis(
    host=celery_settings.REDIS_HOST,
    port=celery_settings.REDIS_PORT,
    decode_responses=True,
)


_conversation_service = ConversationService(
    redis=_redis,
)



# ------------------------------------------------------------------
# Core Services (Singletons)
# ------------------------------------------------------------------

_embedding_service = EmbeddingService()

_search_service = AzureSearchService()

_content_safety_service = ContentSafetyAgent()
_llm = get_llm_service()


_generation_agent = GenerationAgent(_llm)

_document_intelligence_service=DocumentIntelligenceService()




# ------------------------------------------------------------------
# Retrieval Components (Singletons)
# ------------------------------------------------------------------

_query_expander = QueryExpander(_llm)

_hybrid_searcher = HybridSearcher(
    _search_service.client,
    _embedding_service
)

_rrf = ReciprocalRankFusion()

_deduplicator = Deduplicator()

_parent_expander=ParentExpander(_search_service)


_reranker = Reranker(
    _search_service
)
_context_builder=ContextBuilder()

_retriever = Retriever(
    _query_expander,
    _hybrid_searcher,
    _rrf,
    _deduplicator,
    _reranker,
    _parent_expander,
    _context_builder

)

_grounding_agent = GroundingAgent(_llm)

_blob=BlobStorageService()

_document_service = DocumentService(
    blob_storage=_blob,
)











def get_graph():
    return _graph


def get_grounding_agent():
    return _grounding_agent


# ------------------------------------------------------------------
# Dependency Getters
# ------------------------------------------------------------------

def get_embedding_service():
    return _embedding_service


def get_search_service():
    return _search_service


def get_content_safety():
    return _content_safety_service


def get_generation_agent():
    return _generation_agent


def get_llm():
    return _llm


def get_retriever():
    return _retriever
def get_blob():
    return _blob
def get_document_service():

    return _document_service
def get_document_intelligence():
    return _document_intelligence_service
_ingestion_service = IngestionService(
    blob_storage=get_blob(),
    document_intelligence=get_document_intelligence(),
    embedding_service=get_embedding_service(),
    search_service=get_search_service(),
)

def get_ingestion_service() -> IngestionService:
    return _ingestion_service

_nodes = Nodes(
    content_agent=_content_safety_service,
    generation_agent=_generation_agent,
    retrieval_agent=_retriever,
    grounding_agent=_grounding_agent,
)

def get_nodes() -> Nodes:
    return _nodes
def get_chat_service():
    from rag_interview.graph.workflow import app_graph
    return ChatService(
        graph=app_graph,
        nodes=get_nodes(),
        conversation_service=get_conversation_service()
    )
def get_conversation_service() -> ConversationService:
    return _conversation_service
