repository_memory = {}
repositories = repository_memory


def save_repository(
    repository_id,
    owner,
    vector_store,
    documents,
    summary
):
    repository_memory[repository_id] = {
        "owner": owner,
        "documents": documents,
        "vector_store": vector_store,
        "summary": summary
    }


def get_repository(repository_id):
    return repository_memory.get(repository_id)
