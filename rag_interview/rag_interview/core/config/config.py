from pydantic_settings import BaseSettings,SettingsConfigDict

_base_config=SettingsConfigDict(
    env_file=".env",
    env_ignore_empty=True,
    extra="ignore"

)
class Settings(BaseSettings):
   model_config= _base_config
   pass 
class DocSettings(Settings):
    DOCUMENT_INTELLIGENT_KEY: str
    DOCUMENT_INTELLIGENT_ENDPOINT: str
class OpenAISettings(Settings):
    AZURE_OPENAI_ENDPOINT:str
    AZURE_OPENAI_API_KEY:str
    AZURE_OPENAI_API_VERSION:str
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT: str
class SearchSettings(Settings):
    AZURE_SEARCH_ENDPOINT:str
    AZURE_SEARCH_KEY: str
class LLMSettings(Settings):
    AZURE_LLM_ENDPOINT: str
    AZURE_LLM_KEY: str
    AZURE_LLM_DEPLOYMENT: str
    AZURE_LLM_API_VERSION: str
class ContentSafetySettings(Settings):
    CONTENT_SAFETY_ENDPOINT: str
    CONTENT_SAFETY_KEY: str
class EntraSettings(Settings):
    ENTRA_TENANT_ID: str
    ENTRA_CLIENT_ID: str
    ENTRA_AUDIENCE: str
    CLIENT_SECRET: str
class BlobSettings(Settings):
    STORAGE_CONNECTION_STRING: str
    STORAGE_CONTAINER: str
class CelerySettings(Settings):
    REDIS_HOST: str
    REDIS_PORT: str

    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str



    
docsettings=DocSettings()
open_ai_settings=OpenAISettings()
search_settings=SearchSettings()
llm_settings=LLMSettings()
content_safety_settings=ContentSafetySettings()
entrasettings=EntraSettings()
blobsettings=BlobSettings()
celery_settings=CelerySettings()

