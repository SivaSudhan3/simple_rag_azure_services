from langchain_core.prompts import ChatPromptTemplate


GROUNDING_PROMPT = ChatPromptTemplate.from_messages(

    [

        (

            "system",

            """
You are an evaluator.

Compare the answer with the retrieved context.

Return ONLY valid JSON.

Example:

{{
    "grounded_score":0.95,
    "relevance_score":0.90,
    "reason":"Answer is completely supported."
}}
"""

        ),

        (

            "human",

            """
Question:

{question}


Context:

{context}


Answer:

{answer}

"""

        )

    ]

)