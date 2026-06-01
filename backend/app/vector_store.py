from groq import Groq
from langchain.embeddings.base import Embeddings
from langchain_community.vectorstores import FAISS

from app.config import (
    FAISS_PATH,
    GROQ_API_KEY,
    GROQ_EMBEDDING_MODEL,
    TOP_K_RESULTS,
)

class GroqEmbeddings(Embeddings):
    def __init__(self, api_key: str, model: str):
        self.client = Groq(api_key=api_key)
        self.model = model

    def _create_embeddings(self, texts: list[str]) -> list[list[float]]:
        response = self.client.embeddings.create(
            input=texts,
            model=self.model,
            encoding_format="float",
        )
        data = response.data
        if isinstance(data, list):
            return [item.embedding for item in data]
        return [data.embedding]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self._create_embeddings(texts)

    def embed_query(self, text: str) -> list[float]:
        return self._create_embeddings([text])[0]

# Embedding model
embeddings = GroqEmbeddings(
    api_key=GROQ_API_KEY,
    model=GROQ_EMBEDDING_MODEL,
)

# Load FAISS
vectorstore = FAISS.load_local(
    FAISS_PATH,
    embeddings,
    allow_dangerous_deserialization=True,
)

# Retriever
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": TOP_K_RESULTS,
    },
)