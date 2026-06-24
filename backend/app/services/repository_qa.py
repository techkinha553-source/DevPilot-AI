from app.services.context_builder import build_context
from app.services.openai_service import ask_openai


def answer_repository_question(
    repo,
    question: str,
    previous_memory: list = None
):
    if previous_memory is None:
        previous_memory = []
    
    context = build_context(
        question,
        repo["vector_store"]
    )

    memory_context = ""

    for item in previous_memory[-5:]:

        memory_context += f"""
            Question:
            {item['question']}

            Answer:
            {item['answer']}
        """

        prompt = f"""
            Previous Conversation:

            {memory_context}

            Repository Context:

            {context}

            Current Question:

            {question}

            Answer using both the repository
            context and conversation history.
        """

    return ask_openai(prompt)
