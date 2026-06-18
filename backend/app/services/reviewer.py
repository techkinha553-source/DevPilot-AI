from app.services.openai_service import get_client

client = get_client()

def review_code(code: str) -> str:
    response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {
                "role": "system",
                "content": (
                    "Review the code for bugs, readability, "
                    "security issues, and improvements."
                ),
            },
            {
                "role": "user",
                "content": code,
            },
        ],
    )

    return response.choices[0].message.content