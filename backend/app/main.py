from fastapi import FastAPI

from fastapi.middleware.cors import (
    CORSMiddleware
)

from app.models import QueryRequest

from app.rag_pipeline import ask_rag

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mrc-phks.onrender.com", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():

    return {
        "message":
        "Insurance RAG API Running"
    }

@app.post("/ask")
async def ask_question(
    request: QueryRequest
):

    response = ask_rag(
        request.query,
        request.history
    )

    return response