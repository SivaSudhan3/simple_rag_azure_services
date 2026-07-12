class ContextEnricher:


    def enrich(
        self,
        blocks
    ):


        enriched=[]


        for i, block in enumerate(blocks):


            if block.content_type in [
                "table",
                "image"
            ]:


                previous_context = (

                    blocks[i-1].content

                    if i > 0

                    else ""

                )


                next_context = (

                    blocks[i+1].content

                    if i < len(blocks)-1

                    else ""

                )


                block.content = f"""


                Previous Context:

                {previous_context}


                Actual Content:

                {block.content}


                Following Context:

                {next_context}

                """


            enriched.append(
                block
            )


        return enriched