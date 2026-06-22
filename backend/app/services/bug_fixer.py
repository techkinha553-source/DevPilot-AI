def generate_fixes(documents):

    fixes = []

    for doc in documents:

        content = doc["content"]

        if "except:" in content:
            fixes.append({
                "file": doc["path"],
                "fix":
                "Replace bare except with specific exception"
            })

        if "password=" in content.lower():
            fixes.append({
                "file": doc["path"],
                "fix":
                "Move password into environment variables"
            })

    return fixes