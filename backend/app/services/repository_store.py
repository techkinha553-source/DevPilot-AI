repository_memory = {}


def save_repository(
    repository_id,
    vector_store,
    documents
):
    repository_memory[repository_id] = {
        "vector_store": vector_store,
        "documents": documents
    }


def get_repository(repository_id):
    return repository_memory.get(repository_id)
