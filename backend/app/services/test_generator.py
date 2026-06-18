from app.services.openai_service import get_client

client = get_client()

def generate_tests(code: str) -> str:
    response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {
                "role": "system",
                "content": (
                    "Generate comprehensive unit tests "
                    "for the supplied code."
                ),
            },
            {
                "role": "user",
                "content": code,
            },
        ],
    )

    return response.choices[0].message.content