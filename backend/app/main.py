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
    allow_origins=[
        "https://mrc-phks.onrender.com",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "MSDS RAG API Running"
    }

@app.post("/ask")
async def ask_question(request: QueryRequest):
    try:
        response = ask_rag(request.query, request.history)
        return response
    except Exception as exc:
        # If the backend fails, return clean JSON and preserve CORS headers.
        from fastapi import HTTPException

        raise HTTPException(status_code=502, detail=str(exc)) from exc