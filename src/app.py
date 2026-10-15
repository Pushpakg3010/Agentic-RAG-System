from fastapi import FastAPI
from pydantic import BaseModel

from src.graph import graph_app

app = FastAPI()


class Query(BaseModel):
    message: str
    thread_id: str = "default"


@app.post("/chat")
def chat(query: Query):
    config = {"configurable": {"thread_id": query.thread_id}}

    result = graph_app.invoke(
        {"input": query.message},
        config=config
    )

    return {"response": result.get("response", "No response generated.")}