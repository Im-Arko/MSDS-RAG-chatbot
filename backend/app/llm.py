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


_dify_endpoint = None


def _build_dify_payload(prompt: str, endpoint: str):
    if endpoint.endswith("/chat-messages") or "/chat-messages" in endpoint:
        return {
            "inputs": {},
            "query": prompt,
        }

    if endpoint.endswith("/completion-messages") or "/completion-messages" in endpoint:
        return {
            "inputs": {"text": prompt},
        }

    if endpoint.endswith("/chat/completions") or "/openai/v1/chat/completions" in endpoint or "/v1/chat/completions" in endpoint:
        return {
            "model": LLM_MODEL,
            "messages": [{"role": "user", "content": prompt}],
        }

    return {
        "model": LLM_MODEL,
        "messages": [{"role": "user", "content": prompt}],
    }


def _resolve_dify_endpoint():
    global _dify_endpoint
    if _dify_endpoint is not None:
        return _dify_endpoint

    base_url = DIFY_API_URL.rstrip("/")
    if base_url.endswith("/chat-messages") or base_url.endswith("/completion-messages") or base_url.endswith("/chat/completions") or base_url.endswith("/completions"):
        _dify_endpoint = base_url
        return _dify_endpoint

    candidates = [
        base_url + "/chat-messages",
        base_url + "/completion-messages",
        base_url + "/chat/completions",
        base_url + "/completions",
        base_url + "/openai/v1/chat/completions",
        base_url + "/openai/v1/completions",
        base_url + "/v1/chat/completions",
        base_url + "/v1/completions",
        base_url,
    ]

    for candidate in candidates:
        payload = _build_dify_payload("test", candidate)
        try:
            response = requests.post(candidate, json=payload, headers={
                "Authorization": f"Bearer {DIFY_API_KEY}",
                "Content-Type": "application/json",
            }, timeout=10)
            if response.status_code == 404:
                continue
            if response.status_code < 400:
                _dify_endpoint = candidate
                return _dify_endpoint
        except requests.RequestException:
            continue

    raise RuntimeError(
        f"Unable to resolve a valid Dify endpoint from DIFY_API_URL={DIFY_API_URL}."
    )


def _generate_response_with_dify(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json",
    }

    url = _resolve_dify_endpoint()
    payload = _build_dify_payload(prompt, url)

    response = requests.post(url, json=payload, headers=headers, timeout=30)
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        raise RuntimeError(
            f"Dify request failed ({response.status_code}) for {url}: {response.text}"
        ) from exc

    data = response.json()

    if isinstance(data, dict):
        if data.get("choices") and data["choices"]:
            return data["choices"][0].get("message", {}).get("content", "")
        if data.get("output"):
            output = data["output"]
            if isinstance(output, list) and output:
                return str(output[0].get("content", ""))
        if data.get("result"):
            return str(data["result"])
        if data.get("output_text"):
            return str(data["output_text"])

    raise RuntimeError("Dify did not return a valid response.")


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
