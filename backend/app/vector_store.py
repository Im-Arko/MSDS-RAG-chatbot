from langchain_huggingface import (
    HuggingFaceEmbeddings
)

from langchain_community.vectorstores import (
    FAISS
)

from app.config import (
    EMBEDDING_MODEL,
    FAISS_PATH,
    TOP_K_RESULTS
)

# Embedding model
embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)

# Load FAISS
vectorstore = FAISS.load_local(
    FAISS_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)

# Retriever
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": TOP_K_RESULTS
    }
)