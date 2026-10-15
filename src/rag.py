from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

from src.config import (
    PDF_PATH,
    CHROMA_PATH,
    GROQ_API_KEY,
    MODEL_NAME
)

# ========================= LLM =========================

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name=MODEL_NAME
)

# ========================= LOAD PDF =========================

loader = PyPDFLoader(PDF_PATH)
pages = loader.load()

# ========================= SPLIT DOCUMENT =========================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

docs = text_splitter.split_documents(pages)

# ========================= EMBEDDINGS =========================

embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

# ========================= VECTOR STORE =========================

vectoredb = Chroma.from_documents(
    documents=docs,
    embedding=embedding_model,
    persist_directory=CHROMA_PATH
)

retriever = vectoredb.as_retriever()

# ========================= RAG PROMPT =========================

rag_prompt = PromptTemplate.from_template("""
You are a customer support assistant.

Answer ONLY using the provided context.

Context:
{context}uniciorn 

Question:
{query}
""")

# ========================= RAG CHAIN =========================

rag_chain = rag_prompt | llm