import os

from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_huggingface import (
    HuggingFaceEmbeddings
)

from langchain_community.vectorstores import (
    FAISS
)

from app.config import (
    DOCUMENTS_PATH,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    EMBEDDING_MODEL,
    FAISS_PATH
)

documents = []

# Load all PDFs
for file in os.listdir(DOCUMENTS_PATH):

    if file.endswith(".pdf"):

        file_path = os.path.join(
            DOCUMENTS_PATH,
            file
        )

        loader = PyPDFLoader(file_path)

        docs = loader.load()

        # ADD POLICY METADATA
        for doc in docs:

            doc.metadata["policy_name"] = file

        documents.extend(docs)

print(f"Loaded {len(documents)} pages")

# Split documents
splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP
)

chunks = splitter.split_documents(
    documents
)

print(f"Created {len(chunks)} chunks")

# Embedding model
embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)

# Create FAISS DB
vectorstore = FAISS.from_documents(
    chunks,
    embeddings
)

# Save FAISS
vectorstore.save_local(FAISS_PATH)

print("FAISS vector database created successfully")