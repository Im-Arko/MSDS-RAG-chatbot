from fastapi import FastAPI
import requests
from app.config import (
    DIFY_API_KEY,
    DIFY_API_URL,
)
from fastapi.middleware.cors import (
    CORSMiddleware
)

from app.models import QueryRequest

# from app.rag_pipeline import ask_rag

print("MAIN IMPORT URL:", repr(DIFY_API_URL))

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

#def ask_dify(query):
#     payload = {
#         "inputs": {},
#         "query": query,
#         "response_mode": "blocking",
#         "user": "web-user"
#     }
#     print("Calling Dify...")
#     response = requests.post(
#         DIFY_API_URL,
#         headers={
#             "Authorization": f"Bearer {DIFY_API_KEY}",
#             "Content-Type": "application/json"
#         },
#         json=payload,
#         timeout=120
#     )
#     print("Dify responded")
#     response.raise_for_status()

#     return response.json()

# def ask_dify(query):
#     print("URL:", DIFY_API_URL)

#     payload = {
#         "inputs": {},
#         "query": query,
#         "response_mode": "blocking",
#         "user": "web-user"
#     }

#     print("PAYLOAD:", payload)

#     response = requests.post(
#         DIFY_API_URL,
#         headers={
#             "Authorization": f"Bearer {DIFY_API_KEY}",
#             "Content-Type": "application/json"
#         },
#         json=payload,
#         timeout=120
#     )

#     print("STATUS:", response.status_code)
#     print("TEXT:", response.text)

#     response.raise_for_status()

#     return response.json()

# def ask_dify(query):
#     payload = {
#         "inputs": {},
#         "query": query,
#         "response_mode": "blocking",
#         "conversation_id": "",
#         "user": "web-user"
#     }

#     print("URL =", repr(DIFY_API_URL))
#     print("KEY EXISTS =", bool(DIFY_API_KEY))
#     print("PAYLOAD =", payload)

#     try:
#         response = requests.post(
#             DIFY_API_URL,
#             headers={
#                 "Authorization": f"Bearer {DIFY_API_KEY}",
#                 "Content-Type": "application/json",
#             },
#             json=payload,
#             timeout=120,
#         )

#         print("STATUS =", response.status_code)
#         print("BODY =", response.text)

#         response.raise_for_status()

#         data = response.json()

#         return {
#             "answer": data.get("answer", "No answer returned")
#         }
#     except Exception as e:
#             print("EXCEPTION:", repr(e))
#             raise
# def ask_dify(query):
#     print("========== ASK_DIFY ==========")
#     print("DIFY_API_URL:", repr(DIFY_API_URL))
#     print("DIFY_API_KEY exists:", bool(DIFY_API_KEY))
#     print("Query:", query)  

#     return {
#         "answer": "debug"
#     }

def ask_dify(query):
    print("========== ASK_DIFY ==========")
    print("URL:", repr(DIFY_API_URL))
    print("KEY EXISTS:", bool(DIFY_API_KEY))

    payload = {
        "inputs": {},
        "query": query,
        "response_mode": "blocking",
        "conversation_id": "",
        "user": "web-user"
    }

    print("PAYLOAD:", payload)

    try:
        response = requests.post(
            DIFY_API_URL,
            headers={
                "Authorization": f"Bearer {DIFY_API_KEY}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=120
        )

        print("STATUS:", response.status_code)
        print("BODY:", response.text[:2000])

        response.raise_for_status()

        return {
            "answer": response.json().get("answer", "No answer")
        }

    except Exception as e:
        print("EXCEPTION:", repr(e))
        raise

@app.get("/")
async def root():
    return {
        "message": "MSDS RAG API Running"
    }

@app.post("/ask")
async def ask_question(request: QueryRequest):
    try:
        # response = ask_rag(request.query, request.history)
        # response = ask_rag(request.query)
        # return response
        return ask_dify(request.query)
    except Exception as exc:
        # If the backend fails, return clean JSON and preserve CORS headers.
        from fastapi import HTTPException

        raise HTTPException(status_code=502, detail=str(exc)) from exc