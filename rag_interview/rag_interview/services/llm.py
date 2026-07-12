from langchain_openai import AzureChatOpenAI

from rag_interview.core.config.config import (
    llm_settings
)
from langchain_core.messages import AIMessageChunk

class LLMService:


    def __init__(
        self
    ):


        self.llm = AzureChatOpenAI(

    azure_endpoint= llm_settings.AZURE_LLM_ENDPOINT,
    api_key=llm_settings.AZURE_LLM_KEY,
    
    azure_deployment=llm_settings.AZURE_LLM_DEPLOYMENT,
    api_version=llm_settings.AZURE_LLM_API_VERSION,
    
    


        )


    async def generate(
        self,
        prompt
    ):


        response = (
            await self.llm
            .ainvoke(
                prompt
            )
        )


        return response.content
    async def stream(
        self,
        prompt,
    ):
        async for chunk in self.llm.astream(prompt):

            if isinstance(chunk, AIMessageChunk):

                if chunk.content:
                    yield chunk.content
_llm_service=None
def get_llm_service():
    global _llm_service
    if _llm_service is None:
        _llm_service=LLMService()
    return _llm_service



