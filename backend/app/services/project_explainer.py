from ollama import chat


def explain_project(documents):

    content = "\n\n".join(
        doc["content"][:1000]
        for doc in documents[:20]
    )

    response = chat(
        model="qwen3",
        messages=[
            {
                "role": "user",
                "content":
                f"""
                Explain this repository.

                {content}
                """
            }
        ]
    )

    return response.message.content
