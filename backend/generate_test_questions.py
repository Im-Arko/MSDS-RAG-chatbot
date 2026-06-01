# The code below is used to generate realistic user questions based on the content of the MSDS documents, which can be helpful for testing and improving the chatbot's performance.
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from app.llm import generate_response

EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"

# Load FAISS
embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)

db = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

# Retrieve representative MSDS content
docs = db.similarity_search(
    "first aid PPE handling storage spill fire disposal transport",
    k=10
)

context = "\n\n".join(
    doc.page_content
    for doc in docs
)

prompt = f"""
You are an industrial safety expert.

Based ONLY on the MSDS content below, generate 50 realistic questions that users might ask an MSDS chatbot.

Requirements:

- Questions must be answerable from the documents.
- Include:
    - First aid
    - PPE
    - Handling
    - Storage
    - Fire fighting
    - Spill response
    - Disposal
    - Transport
    - Environmental hazards
    - Health hazards

- Use actual product names if mentioned.
- Make questions realistic and concise.
- Return only the questions.

MSDS Content:

{context}
"""

questions = generate_response(prompt)

print("\nGENERATED QUESTIONS:\n")
print(questions)