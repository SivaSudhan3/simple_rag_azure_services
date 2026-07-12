from agents.security.content_safety_agent import ContentSafetyAgent

from agents.security.prompt_injection_agent import PromptInjectionAgent
from graph.graph_schema import GraphSchema



content_agent = ContentSafetyAgent()

prompt_agent = PromptInjectionAgent()



def security_node(state:GraphSchema):


    content_result = (
        content_agent
        .analyze(
            state["question"]
        )
    )


    attack_result = (
        prompt_agent
        .scan(
            state["question"]
        )
    )


    if (
        not content_result["safe"]
        or
        attack_result["attack"]
    ):


        state["is_safe"] = False


        state["blocked_reason"] = {

            "content":
            content_result,


            "prompt":
            attack_result

        }


        return state



    state["is_safe"]=True


    return state