from pydantic import BaseModel, Field


class TimingMetrics(BaseModel):
    # Retrieval
    query_expansion_ms: float = 0.0
    embedding_ms: float = 0.0
    lexical_search_ms: float = 0.0
    vector_search_ms: float = 0.0
    semantic_ranking_ms: float = 0.0
    parent_expansion_ms: float = 0.0
    context_build_ms: float = 0.0
    retrieval_total_ms: float = 0.0

    # Generation
    generation_startup_ms: float = 0.0
    ttft_ms: float = 0.0
    generation_ms: float = 0.0
    total_request_ms: float = 0.0

    # Ingestion
    document_analysis_ms: float = 0.0
    chunking_ms: float = 0.0
    embedding_generation_ms: float = 0.0
    indexing_ms: float = 0.0
    ingestion_total_ms: float = 0.0


class RetrievalMetrics(BaseModel):
    expanded_queries: int = 0

    lexical_results: int = 0
    vector_results: int = 0
    semantic_results: int = 0

    final_documents: int = 0

    context_characters: int = 0
    estimated_context_tokens: int = 0


class TokenMetrics(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class IngestionMetrics(BaseModel):
    documents_processed: int = 0
    pages_processed: int = 0
    chunks_created: int = 0
    embeddings_generated: int = 0
    vectors_indexed: int = 0


class TelemetryMetrics(BaseModel):
    timings: TimingMetrics = Field(default_factory=TimingMetrics)
    retrieval: RetrievalMetrics = Field(default_factory=RetrievalMetrics)
    tokens: TokenMetrics = Field(default_factory=TokenMetrics)
    ingestion: IngestionMetrics = Field(default_factory=IngestionMetrics)