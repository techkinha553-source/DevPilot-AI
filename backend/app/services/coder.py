from app.services.openai_service import get_client

client = get_client()

def generate_code(task: str, context: str) -> str:
    response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert software engineer. "
                    "Generate clean, maintainable code."
                ),
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nTask:\n{task}",
            },
        ],
    )

    return response.choices[0].message.content