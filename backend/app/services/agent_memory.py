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


# Backward compatibility aliases
# Older agent modules may import save_memory3/get_memory3

def save_memory3(
    repository_id,
    question,
    answer
):
    return save_memory(
        repository_id,
        question,
        answer
    )


def get_memory3(repository_id):
    return get_memory(repository_id)