class ReciprocalRankFusion:


    def fuse(
        self,
        result_sets,
        k=60
    ):


        scores = {}

        docs = {}



        for results in result_sets:


            for rank,doc in enumerate(results):


                doc_id = (
                    doc["id"]
                )


                docs[doc_id]=doc


                if doc_id not in scores:


                    scores[doc_id]=0



                scores[doc_id]+=(
                    1 /
                    (
                    k + rank + 1
                    )
                )



        ranked = sorted(

            scores.items(),

            key=lambda x:x[1],

            reverse=True

        )


        return [

            docs[id]

            for id,score in ranked

        ]