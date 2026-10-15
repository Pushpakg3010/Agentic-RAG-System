from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from src.state import AgentState



from src.nodes import (
    start_router_node,
    classify_intent_node,
    check_order_id_node,
    ask_order_id_node,
    fetch_order_id_node,
    rag_node,
)
from langgraph.checkpoint.memory import MemorySaver

from src.routers import (
    start_router_decision,
    intent_router,
    order_id_router
)
# =========================BUILD GRAPH================================
graph= StateGraph(AgentState)

graph.add_node("start_router", start_router_node)
graph.add_node("classify_route",classify_intent_node)
graph.add_node("check_order_id",check_order_id_node)
graph.add_node("ask_order_id",ask_order_id_node)
graph.add_node("fetch_order", fetch_order_id_node)
graph.add_node("rag_node", rag_node)

graph.add_edge(START, "start_router")
graph.add_conditional_edges("start_router",
                            start_router_decision, # Use the separate router function
                            {
                                "check_order_id":"check_order_id",
                                "classify_route":"classify_route"
                            })

graph.add_conditional_edges("classify_route",
                            intent_router,
                            {
                                "rag_node":"rag_node",
                                "check_order_id":"check_order_id",
                                END:END
                            }
                            )
graph.add_conditional_edges("check_order_id",
                            order_id_router,
                            {
                                "ask_order_id":"ask_order_id",
                                "fetch_order":"fetch_order"
                            }
                            )

graph.add_edge("ask_order_id",END)
graph.add_edge("fetch_order",END)
graph.add_edge("rag_node",END)


#----------------PERSISTENCE----------------------------------------------
memory= MemorySaver()

# --------------------- COMPILE GRAPH---------------------------
graph_app=graph.compile(checkpointer=memory)