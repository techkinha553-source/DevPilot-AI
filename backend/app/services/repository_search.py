def search_repository(
    vector_store,
    query_embedding,
    k=10
):
    results = vector_store.search(
        query_embedding,
        k=k
    )

    formatted = []

    for result in results:

        formatted.append(
            {
                "path": result.get(
                    "path",
                    "Unknown"
                ),
                "content_preview":
                    result.get(
                        "content",
                        ""
                    )[:500]
            }
        )

    return formatted