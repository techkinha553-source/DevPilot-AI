def generate_documentation(documents):

    documentation = []

    for doc in documents:

        path = doc.get("path", "")

        if path.endswith((
            ".py",
            ".js",
            ".ts",
            ".tsx"
        )):

            content = doc.get("content", "")

            functions = []

            for line in content.splitlines():

                line = line.strip()

                if line.startswith("def "):
                    functions.append(line)

                elif line.startswith("function "):
                    functions.append(line)

                elif "=>" in line:
                    functions.append(line)

            documentation.append({
                "file": path,
                "functions": functions[:20]
            })

    return documentation
