from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "openai/gpt-oss-20b"

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = str(BASE_DIR / "data" / "order.db")
PDF_PATH = str(BASE_DIR / "data" / "Amazon Services Business Solutions Agreement.pdf")

if os.getenv("VERCEL") == "1":
    CHROMA_PATH = "/tmp/chroma_db"
else:
    CHROMA_PATH = str(BASE_DIR / "chroma_db")
