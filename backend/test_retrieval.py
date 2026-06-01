from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-base-en-v1.5"
)

db = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

results = db.similarity_search(
    "What PPE is required when handling acetone?",
    k=5
)

for i, doc in enumerate(results, 1):
    print(f"\n=== Result {i} ===")
    print(doc.metadata)
    print(doc.page_content[:500])