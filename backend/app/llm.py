import requests

from app.config import (
    DIFY_API_KEY,
    DIFY_API_URL,
    GROQ_API_KEY,
    LLM_MODEL,
    USE_DIFY,
)

if not USE_DIFY:
    from groq import Groq

    client = Groq(
        api_key=GROQ_API_KEY
    )


def _generate_response_with_dify(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
    }
    url = DIFY_API_URL.rstrip("/") + "/chat/completions"

    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()

    return data["choices"][0]["message"]["content"]


def _generate_response_with_groq(prompt: str) -> str:
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


def generate_response(prompt: str) -> str:
    if USE_DIFY:
        return _generate_response_with_dify(prompt)

    return _generate_response_with_groq(prompt)
