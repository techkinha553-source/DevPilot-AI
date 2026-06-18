import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")
    return OpenAI(api_key=api_key)


def ask_codebase(question: str, documents: list[dict]) -> str:
    context_parts = []

    # Limit context to avoid huge prompts
    for doc in documents[:20]:
        context_parts.append(
            f"FILE: {doc['path']}\n{doc['content']}"
        )

    context = "\n\n".join(context_parts)
    client = get_client()

    prompt = f"""
You are an expert software engineer.

Below is the repository content.

{context}

Question:
{question}

Answer only using information from the repository when possible.
"""

    response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {
                "role": "system",
                "content": "You are an expert code assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content
