repository_memory = {}


def save_repository(
    repository_id,
    vector_store,
    documents,
    summary
):
    repository_memory[repository_id] = {
        "vector_store": vector_store,
        "documents": documents,
        "summary": summary
    }


def get_repository(repository_id):
    return repository_memory.get(repository_id)
