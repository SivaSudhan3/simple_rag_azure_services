from rag_interview.graph.graph_schema import GraphSchema
from langgraph.graph import StateGraph,END
from rag_interview.core.dependencies import get_nodes
from rag_interview.graph.routers import safety_router

node=get_nodes()

workflow=StateGraph(GraphSchema)
workflow.add_node(
    "security",
    node.security_node
)
workflow.add_node(
    "grounding",
    node.grounding_node
)
workflow.add_node(
    "retriever",
    node.retrieval_node
)
workflow.add_node(
    "blocked",
    node.blocked_node
)
workflow.add_node(
    "generator",
    node.generation_node
)

workflow.set_entry_point(
    "security"
)
workflow.add_conditional_edges(
    "security",
    safety_router,
    {
        "rag":"retriever",
        "blocked":"blocked"

    }

)
workflow.add_edge("retriever","generator")
workflow.add_edge("generator","grounding")
workflow.add_edge("grounding",END)


workflow.add_edge(
    "blocked",
    END
)


app_graph = workflow.compile()