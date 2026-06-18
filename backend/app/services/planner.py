from app.services.openai_service import get_client

client = get_client()

def create_plan(task: str) -> str:
    response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a senior software architect. "
                    "Break the request into clear implementation steps."
                ),
            },
            {
                "role": "user",
                "content": task,
            },
        ],
    )

    return response.choices[0].message.content