from langchain_openai import AzureChatOpenAI


class QueryExpander:


    def __init__(
        self,
        llm: AzureChatOpenAI
    ):

        self.llm = llm



    async def expand(
        self,
        question: str,
        chat_history: list[dict] | None = None,

    ):

        history = ""

        if chat_history:

            history = "\n".join(

                f"{message['role']}: {message['content']}"

                for message in chat_history

            )
        prompt = f"""
            You are a query rewriting assistant.

            Conversation History:
            {history}

            Current Question:
            {question}

            If the current question depends on previous conversation,
            rewrite it into standalone search queries.

            Generate 3 search queries.

            Keep the intent exactly the same.

            Return only the queries.

            One query per line.
            """



        response = (
            await self.llm.generate(
                prompt
            )
        )


       

        queries = [

        q.strip()

        for q
        in response.split("\n")

        if q.strip()

        ]

        # Include original question and remove duplicates
        unique_queries = []

        for query in [question] + queries:

            if query not in unique_queries:

                unique_queries.append(query)

        return unique_queries

