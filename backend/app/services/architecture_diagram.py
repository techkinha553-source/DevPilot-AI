def generate_architecture_diagram(repo):

    components = set()
    relationships = []

    documents = repo["documents"]

    for doc in documents:

        path = doc.get("path", "")

        if "/api/" in path:
            components.add("FastAPI")

        if "vector_store" in path.lower():
            components.add("FAISS")

        if "openai" in path.lower():
            components.add("LLM Service")

        if "repository" in path.lower():
            components.add("Repository Store")

    components = list(components)

    if "FastAPI" in components and "Repository Store" in components:
        relationships.append(
            "FastAPI -> Repository Store"
        )

    if "FastAPI" in components and "LLM Service" in components:
        relationships.append(
            "FastAPI -> LLM Service"
        )

    if "Repository Store" in components and "FAISS" in components:
        relationships.append(
            "Repository Store -> FAISS"
        )

    return {
        "agent": "architecture-generator",
        "components": components,
        "relationships": relationships
    }