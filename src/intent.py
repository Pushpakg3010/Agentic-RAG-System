from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

from src.config import GROQ_API_KEY, MODEL_NAME

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name=MODEL_NAME,
)



# ====================LLM BASED INTENT CLASSIFICATION PROMPT========
intent_prompt = PromptTemplate.from_template("""
you are a smart customer-support router.

your task:
Decide where the answer existes.

Return ONLY:

policy
OR
db

use:

policy:
- refund
-return policy
-warranty
-cancellation
-terms
-agreement
-policy questions

db:
-track order
-delivery
-shipment
-where is my order
-order status
-tracking

User Query:
{query}

Answer
""")


intent_chain = intent_prompt |llm