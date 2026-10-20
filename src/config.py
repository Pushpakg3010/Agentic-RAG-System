from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY =os.getenv("GROQ_API_KEY")

# =========================
# Model
# =========================
MODEL_NAME = "openai/gpt-oss-20b"

# =========================
# File Paths
# =========================

DATABASE_PATH = "data/order.db"
PDF_PATH = "data/Amazon Services Business Solutions Agreement.pdf"

CHROMA_PATH = "chroma_db"



