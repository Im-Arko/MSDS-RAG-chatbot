from app.vector_store import retriever
from app.llm import generate_response

import os

from app.config import DOCUMENTS_PATH


def ask_rag(question, history):

    question_lower = question.lower()

    # =========================
    # RETRIEVE CHUNKS
    # =========================

    retrieved_docs = retriever.invoke(
        question
    )

    current_policy = None

    # =========================
    # DETECT POLICY
    # =========================

    for file in os.listdir(DOCUMENTS_PATH):

        clean_name = (
            file
            .replace(".pdf", "")
            .replace("_", " ")
            .replace("-", " ")
            .lower()
        )

        # PARTIAL MATCH
        words = clean_name.split()

        match_count = 0

        for word in words:

            if word in question_lower:

                match_count += 1

        if match_count >= 2:

            current_policy = file

            break

    # =========================
    # HISTORY POLICY MEMORY
    # =========================

    if not current_policy:

        for message in reversed(history):

            content = message.get(
                "content",
                ""
            ).lower()

            for file in os.listdir(
                DOCUMENTS_PATH
            ):

                clean_name = (
                    file
                    .replace(".pdf", "")
                    .replace("_", " ")
                    .replace("-", " ")
                    .lower()
                )

                words = clean_name.split()

                match_count = 0

                for word in words:

                    if word in content:

                        match_count += 1

                if match_count >= 2:

                    current_policy = file

                    break

            if current_policy:
                break

    # =========================
    # FILTER RETRIEVED DOCS
    # =========================

    docs = []

    if current_policy:

        for doc in retrieved_docs:

            if (
                doc.metadata.get(
                    "policy_name"
                ) == current_policy
            ):

                docs.append(doc)

    # FALLBACK
    if len(docs) == 0:

        docs = retrieved_docs

    # =========================
    # DEBUGGING
    # =========================

    print("\nACTIVE POLICY:")
    print(current_policy)

    # =========================
    # CONTEXT
    # =========================

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    # =========================
    # MEMORY
    # =========================

    conversation_history = ""

    for message in history[-6:]:

        role = message.get("role")

        content = message.get("content")

        conversation_history += (
            f"{role}: {content}\n"
        )

    # =========================
    # PROMPT
    # =========================

    prompt = f'''
You are a highly accurate insurance policy assistant.

STRICT RULES:
1. Answer ONLY using the provided documents.
2. NEVER use outside insurance knowledge.
3. NEVER guess.
4. If information is missing, say:
"This information is not found in the provided documents."

Conversation History:
{conversation_history}

Documents:
{context}

Question:
{question}
'''

    answer = generate_response(prompt)

    return {
        "answer": answer
    }