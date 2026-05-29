from app.vector_store import vectorstore
from app.llm import generate_response


POLICIES = {
    "easy health": "HDFC-Life-Easy-Health",
    "surgicare": "HDFC-Surgicare",
    "group term": "HDFC-Life-Group-Term-Life",
    "sanchay plus": "HDFC-Life-Sanchay-Plus",
    "smart pension": "HDFC-Life-Smart-Pension",
    "sampoorna jeevan": "HDFC-Life-Sampoorna-Jeevan",
}


def detect_policy(question):

    question_lower = question.lower()

    for policy_key, policy_file in POLICIES.items():

        if policy_key in question_lower:
            return policy_file

    return None


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

    selected_policy = detect_policy(question)

    # retrieve many chunks
    docs = vectorstore.similarity_search(
        question,
        k=100
    )

    # policy filtering
    if selected_policy:

        policy_docs = []

        for doc in docs:

            policy_name = doc.metadata.get(
                "policy_name",
                ""
            )

            if (
                selected_policy.lower()
                in policy_name.lower()
            ):
                policy_docs.append(doc)

        print(
            f"\nUSING POLICY: {selected_policy}"
        )

        print(
            f"FOUND {len(policy_docs)} POLICY CHUNKS"
        )

        if policy_docs:

            policy_docs = sorted(
                policy_docs,
                key=lambda d: rerank_score(
                    d,
                    question
                ),
                reverse=True
            )

            docs = policy_docs[:20]

        else:

            docs = docs[:20]

    else:

        docs = docs[:20]

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
            f"Source: {doc.metadata.get('policy_name', '')}\n{doc.page_content}"
            for doc in docs
        ]
    )

    conversation_history = ""

    for message in history[-6:]:

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
You are a highly accurate insurance policy assistant.

STRICT RULES:

1. Answer ONLY using the provided insurance documents.

2. Do NOT use outside knowledge.

3. Do NOT guess, infer, estimate, or assume.

4.RESPONSE FORMATTING RULES:

Write clear and professional answers.
Use multiple paragraphs when appropriate.
Leave a blank line between paragraphs.

5. If the provided documents contain information relevant to the question, answer using that information.

6. Only reply exactly:
"This information is not found in the provided documents."
when the retrieved context contains no relevant information.

7. Do not mix information from different policies.

8. If a policy name is mentioned in the question, answer only from that policy.

Conversation History:
{conversation_history}

Insurance Documents:
{context}

Question:
{question}
"""

    answer = generate_response(prompt)

    return {
        "answer": answer
    }