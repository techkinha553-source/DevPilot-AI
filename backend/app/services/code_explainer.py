from app.services.openai_service import ask_llm


def explain_repository(documents):

    context = ""

    for doc in documents[:20]:
        context += (
            f"\nFILE: {doc['path']}\n"
            f"{doc['content'][:2000]}"
        )

    prompt = f"""
Explain this repository:

{context}

Provide:
1. Project purpose
2. Architecture
3. Main components
4. Technologies used
"""

    return ask_llm(prompt)