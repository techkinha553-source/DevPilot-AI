def generate_api_docs(documents):

    apis = []

    keywords = [
        "@router.get",
        "@router.post",
        "@router.put",
        "@router.delete",
        "@app.get",
        "@app.post",
        "@app.put",
        "@app.delete"
    ]

    for doc in documents:

        path = doc.get("path", "")

        content = doc.get("content", "")

        endpoints = []

        for line in content.splitlines():

            stripped = line.strip()

            for keyword in keywords:

                if keyword in stripped:
                    endpoints.append(stripped)

        if endpoints:

            apis.append({
                "file": path,
                "endpoints": endpoints
            })

    return apis
