from app.services.openai_service import get_client

client = get_client()

def generate_fix(description):

    response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {
                "role": "system",
                "content":
                "You are an expert debugger."
            },
            {
                "role": "user",
                "content":
                f"Fix this bug: {description}"
            }
        ]
    )
    return response.choices[0].message.content
