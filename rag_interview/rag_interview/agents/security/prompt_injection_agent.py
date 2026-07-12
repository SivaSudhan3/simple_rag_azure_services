class PromptInjectionAgent:


    def __init__(self):

        self.rules=[

            "ignore previous",

            "developer message",

            "system instructions",

            "reveal prompt",

            "bypass"

        ]


    def scan(
        self,
        text
    ):


        detected=[]


        for rule in self.rules:


            if rule in text.lower():


                detected.append(rule)



        return {

            "attack":
                bool(detected),


            "matches":
                detected

        }