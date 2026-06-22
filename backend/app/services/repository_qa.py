from app.services.context_builder import build_context
from app.services.openai_service import ask_openai


def answer_repository_question(
    repo,
    question: str
):
    context = build_context(
        question,
        repo["vector_store"]
    )

    prompt = f"""
Repository Context:

{context}

Question:
{question}

Answer the question using only
the repository context.
"""

    return ask_openai(prompt)