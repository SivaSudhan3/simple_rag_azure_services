from azure.ai.contentsafety import ContentSafetyClient

from azure.core.credentials import AzureKeyCredential



class ContentSafetyAgent:


    def __init__(
        self,
        endpoint,
        key
    ):


        self.client = ContentSafetyClient(

            endpoint,

            AzureKeyCredential(key)

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