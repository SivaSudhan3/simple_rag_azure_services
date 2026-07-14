class ContextBuilder:

    def build(self, documents):

        context = []
        citation_map = {}

        for i, doc in enumerate(documents, start=1):

            citation_map[i] = {
                "id": doc.id,
                "file": doc.source_file,
                "page": doc.page_number,
            }

            context.append(
                f"""
[{i}]
Source File: {doc.source_file}
Page: {doc.page_number}

Content:
{doc.content}
"""
            )
        context = "\n\n".join(context)

        print(context)

        print("=" * 80)
        print(f"Documents : {len(documents)}")
        print(f"Characters: {len(context)}")
        print("=" * 80)

        return {
            "context": context,
            "citation_map": citation_map,
        }