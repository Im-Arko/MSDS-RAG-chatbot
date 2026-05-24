import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Embedding Model
EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"

# LLM Model
LLM_MODEL = "llama-3.1-8b-instant"

# Chunk Settings
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 250

# Retrieval
TOP_K_RESULTS = 10

# Paths
FAISS_PATH = "faiss_index"
DOCUMENTS_PATH = "insurance_docs"