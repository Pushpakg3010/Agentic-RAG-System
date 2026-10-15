

from langgraph.graph import END
from src.state import AgentState
# ============== START ROUTER DECISION ====================

def start_router_decision(state: AgentState):

    if state["route"] == "resume_order_flow":
        return "check_order_id"

    return "classify_route"



def intent_router(state:AgentState):
  route = state["route"]

  if route == "policy":
    return "rag_node"

  elif route == "db":
    return "check_order_id"

  return END



def order_id_router(state:AgentState):
  if state.get("awaiting_order_id"):
    return "ask_order_id"

  return "fetch_order"