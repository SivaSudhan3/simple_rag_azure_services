from azure.ai.contentsafety import ContentSafetyClient

from azure.core.credentials import AzureKeyCredential

from rag_interview.core.config.config import content_safety_settings



class ContentSafetyAgent:


    def __init__(
        self
     
    ):


        self.client = ContentSafetyClient(

            content_safety_settings.CONTENT_SAFETY_ENDPOINT,

            AzureKeyCredential(content_safety_settings.CONTENT_SAFETY_KEY)

        )



    def analyze(
        self,
        text:str
    ):


        response = (
            self.client
            .analyze_text(
                {
                    "text": text
                }
            )
        )


        violations = []


        for item in response.categories_analysis:


            if item.severity >= 4:


                violations.append(
                    item.category
                )


        return {

            "safe":
                len(violations)==0,


            "violations":
                violations

        }