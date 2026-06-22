agent_memory = {}


def save_memory(
    repository_id,
    question,
    answer
):
    if repository_id not in agent_memory:
        agent_memory[repository_id] = []

    agent_memory[repository_id].append({
        "question": question,
        "answer": answer
    })


def get_memory(repository_id):
    return agent_memory.get(
        repository_id,
        []
    )