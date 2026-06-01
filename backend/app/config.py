import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Embedding Model
GROQ_EMBEDDING_MODEL = os.getenv("GROQ_EMBEDDING_MODEL", "nomic-embed-text-v1_5")

# LLM Model
LLM_MODEL = "llama-3.1-8b-instant"

# Chunk Settings
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 250

# Retrieval
TOP_K_RESULTS = 10

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAISS_PATH = os.getenv('FAISS_PATH', os.path.join(BASE_DIR, 'faiss_index'))
DOCUMENTS_PATH = os.getenv(
    'DOCUMENTS_PATH',
    os.path.abspath(os.path.join(BASE_DIR, '..', '..', 'docs')),
)