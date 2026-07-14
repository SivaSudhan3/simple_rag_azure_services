from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)


GENERATION_PROMPT = ChatPromptTemplate.from_messages(

    [

        (
            "system",
            """
You are an enterprise AI assistant.

Answer ONLY from the provided context.

If the answer is not present, say:

"I couldn't find the answer in the provided documents."

Always be factual.
Always format explanations using Markdown.

"""
        ),

        MessagesPlaceholder(
            variable_name="chat_history",
            optional=True
        ),

        (
            "human",
            """
Context:

{context}

Question:

{question}
"""
        )

    ]

)