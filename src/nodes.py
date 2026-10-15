from src.state import AgentState
from src.intent import intent_chain
from src.state import AgentState
from src.intent import intent_chain
from src.rag import rag_chain, retriever
from src.utils import extract_order_id
import sqlite3
# ========================= START ROUTER NODE ================================

def start_router_node(state: AgentState):

    # -------- SYSTEM IS ALREADY WAITING FOR ORDER ID ----------

    if state.get("awaiting_order_id"):
        return {"route": "resume_order_flow"}

    # --------------- NEW QUERY -------------
    return {"route": "new_query"}


# ==================CLASSIFY INTENT NODE=========================

def classify_intent_node(state:AgentState):
  query = state["input"]
  route= intent_chain.invoke({
      "query":query
  }).content.strip().lower()

  return{ "route":route}


 # ======  CHECKING ORDER ID NONE =========================

def check_order_id_node(state:AgentState):
  user_query = state["input"]

  order_id=extract_order_id(user_query)


  # ------------------ORDER ID FOUND----------------------------------
  if order_id: # Corrected: Order_id -> order_id

    return{
        "order_id":order_id,
        "awaiting_order_id":False
    }

  # ---------------------ORDER ID MISSING---------------------------

  return {
      "awaiting_order_id":True # Corrected: awaiting_ordre_id -> awaiting_order_id
  }


# ============== ASK ORDER ID NODE======================================

def ask_order_id_node(state:AgentState):

  return {
      "response":(
          "Please provide your order ID. \n\n"
          "Example:ORD12345"
      ),
      "awaiting_order_id":True
  }



# ========FETCH ORDER ID NODE====================================
import sqlite3
from src.config import DATABASE_PATH

# ======== FETCH ORDER ID NODE ====================================

def fetch_order_id_node(state: AgentState):
    order_id = state["order_id"]

    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT order_id, user_name, status, item
        FROM orders
        WHERE order_id = ?
    """, (order_id,))

    row = cur.fetchone()
    conn.close()

    # ------------------ ORDER FOUND -------------------------------

    if row:

        order_id, user_name, status, item = row

        response = f"""
Hello {user_name},

Your order {order_id}
for {item}
is currently:

{status}
"""

        awaiting_order_id = False

    # ------------------ ORDER NOT FOUND ---------------------------

    else:

        response = f"""
Sorry,

I could not find your order with ID {order_id}.

Please verify your Order ID and try again.
"""

        # Keep waiting so the user can enter another Order ID
        awaiting_order_id = True

    return {
        "response": response,
        "awaiting_order_id": awaiting_order_id
    }


# ===============================RAG NODE==================================

def rag_node(state: AgentState):
    query = state["input"]

    docs = retriever.invoke(query)

    if not docs:
        return {"response": "I could not find relevant information in the policy document."}

    context = "\\n\\n".join([doc.page_content for doc in docs])

    answer = rag_chain.invoke({
        "context": context,
        "query": query
    })

    return {"response": answer.content}