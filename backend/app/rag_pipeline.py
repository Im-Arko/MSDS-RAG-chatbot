from app.vector_store import vectorstore
from app.llm import generate_response

MAX_RETRIEVAL_DOCS = 100
MAX_PROMPT_DOCS = 10
MAX_DOC_CHARS = 1200
MAX_HISTORY_ENTRIES = 4


def rerank_score(doc, question):

    text = doc.page_content.lower()

    score = 0

    try:
        page = int(
            doc.metadata.get(
                "page",
                0
            )
        )
    except:
        page = 0

    # boost later pages
    if page >= 5:
        score += 3

    question_words = set(
        question.lower().split()
    )

    for word in question_words:

        if (
            len(word) > 3
            and word in text
        ):
            score += 1

    return score


def ask_rag(question, history):

    # retrieve relevant chunks
    docs = vectorstore.similarity_search(
        question,
        k=MAX_RETRIEVAL_DOCS
    )

    # rerank and select top documents
    docs = sorted(
        docs,
        key=lambda d: rerank_score(
            d,
            question
        ),
        reverse=True
    )

    docs = docs[:MAX_PROMPT_DOCS]

    print(
        "\n========== RETRIEVED CHUNKS ==========\n"
    )

    for i, doc in enumerate(docs):

        print(
            f"\nCHUNK {i + 1}"
        )

        print(doc.metadata)

        print(
            doc.page_content[:1000]
        )

        print(
            "\n=========================\n"
        )

    context = "\n\n".join(
        [
            doc.page_content if len(doc.page_content) <= MAX_DOC_CHARS else doc.page_content[:MAX_DOC_CHARS] + '\n...[truncated]'
            for doc in docs
        ]
    )

    conversation_history = ""

    for message in history[-MAX_HISTORY_ENTRIES:]:

        role = message.get(
            "role",
            ""
        )

        content = message.get(
            "content",
            ""
        )

        conversation_history += (
            f"{role}: {content}\n"
        )

    prompt = f"""
You are a highly accurate MSDS (Material Safety Data Sheet) assistant.

STRICT RULES:

1. Answer ONLY using the provided MSDS documents.

2. Do NOT use outside knowledge.

3. Do NOT guess, infer, estimate, or assume.

4. RESPONSE FORMATTING RULES:

Write clear and professional answers.
Use multiple paragraphs when appropriate.
Leave a blank line between paragraphs.

5. Do not mention filenames, page numbers, or page locations in your answer.
6. Do not repeat source metadata or context labels unless explicitly requested.
7. If the provided documents contain information relevant to the question, answer using that information and dont repeat the document title mutiple times.

8. Only reply exactly:
"This information is not found in the provided MSDS documents."
when the retrieved context contains no relevant information.

9. Prioritize safety and health information when answering questions about hazards, precautions, or emergency procedures.

Conversation History:
{conversation_history}

MSDS Documents:
{context}

Question:
{question}
"""

    answer = generate_response(prompt)

    return {
        "answer": answer
    }