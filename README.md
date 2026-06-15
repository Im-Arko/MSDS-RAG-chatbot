# MSDS RAG Chatbot

An AI-powered Retrieval-Augmented Generation (RAG) chatbot that enables users to query Material Safety Data Sheets (MSDS) using natural language. The system retrieves relevant information from a vectorized MSDS knowledge base and generates context-aware responses using Large Language Models (LLMs).

## Project Status

🚧 **Development / Prototype Stage**

The frontend is fully functional and deployed but some features dont have backend support yet. The backend implementation is complete and works in local development; however, deployment is currently limited by hosting resource constraints. The application uses local embedding models and a FAISS vector database, which exceed the memory limits of free-tier hosting services.

Future work includes:

* Migrating embeddings to an external embedding API
* Optimizing memory usage
* Deploying the backend on a higher-memory hosting platform

## Features

* Natural language querying of MSDS documents
* Retrieval-Augmented Generation (RAG)
* Semantic search using FAISS
* Conversational chat interface
* Context-aware responses using Groq LLMs
* PDF-based knowledge base processing

## Tech Stack

### Frontend

* React
* Vite
* Tailwind CSS
* Axios

### Backend

* FastAPI
* LangChain
* FAISS
* Sentence Transformers
* Groq

### AI Components

* HuggingFace Embeddings
* Vector Search
* Retrieval-Augmented Generation (RAG)

## Architecture

```text
MSDS PDFs
    ↓
Document Processing
    ↓
Text Chunking
    ↓
Embeddings Generation
    ↓
FAISS Vector Database
    ↓
User Query
    ↓
Semantic Retrieval
    ↓
Groq LLM
    ↓
Generated Response
```

## Current Limitations

* Backend is not publicly deployed due to memory constraints on free-tier hosting platforms.
* Local embedding models require more RAM than available on the selected deployment environment.
* The project currently runs successfully in a local development environment.

## Running Locally

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

To use the Dify backend, add `DIFY_API_KEY` and optionally `DIFY_API_URL` to `backend/.env`:

```bash
DIFY_API_KEY=app-<your-dify-key>
DIFY_API_URL=http://127.0.0.1/v1
```

When `DIFY_API_KEY` is present, the backend will proxy RAG prompts through Dify instead of Groq.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Example Questions

* What are the hazards associated with product X?
* What PPE should be used when handling this chemical X?
* How should product X be stored?
* What are the first aid measures for eye contact?
* Is substance X flammable?
* What should be done in case of a spill of product X?

## Learning Outcomes

This project was developed to explore:

* Retrieval-Augmented Generation (RAG)
* Vector databases and semantic search
* Document question-answering systems
* FastAPI backend development
* React frontend development
* LLM integration using Groq
* Deployment challenges for AI applications

## Future Enhancements

* Production backend deployment
* Citation-based responses
* Streaming answer generation
* Multi-document support
* User authentication
* Admin dashboard for document management

