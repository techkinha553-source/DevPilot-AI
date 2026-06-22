from app.services.openai_service import get_client

client = get_client()

def generate_code(prompt: str):

    response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {
                "role": "system",
                "content":
                "You are a senior software engineer."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.choices[0].message.content
