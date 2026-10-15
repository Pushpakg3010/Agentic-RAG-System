# =====================STATE=====================================
from typing import List, TypedDict


class AgentState(TypedDict):
    input: str
    message: List[str]
    route: str
    response: str
    order_id: str
    awaiting_order_id: bool