from ollama import chat

def ask_codebase(question: str, documents: list[dict]) -> str:
    context_parts = []

    # Limit context to avoid huge prompts
    for doc in documents[:20]:
        context_parts.append(
            f"FILE: {doc['path']}\n{doc['content']}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
            You are an expert software engineer.

            Below is the repository content.

            {context}

            Question:
            {question}

            Answer only using information from the repository when possible.
        """

    response = chat(
        model="qwen3",
        messages=[
            {
                "role": "system",
                "content": "You are an expert code assistant. Answer only from the repository context when possible."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]
