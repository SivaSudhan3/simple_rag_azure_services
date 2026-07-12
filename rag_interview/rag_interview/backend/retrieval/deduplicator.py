class Deduplicator:


    def dedupe(
        self,
        documents
    ):


        seen=set()


        unique=[]



        for doc in documents:


            chunk_id = (
                doc["id"]
            )



            if chunk_id in seen:


                continue



            seen.add(
                chunk_id
            )


            unique.append(
                doc
            )


        return unique