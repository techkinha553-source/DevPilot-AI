def build_context(results):
    context = ""

    for item in results:
        context += f"\nFILE: {item['path']}\n"
        context += item["content"][:2000]
        context += "\n"

    return context