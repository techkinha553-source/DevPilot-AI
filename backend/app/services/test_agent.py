def generate_tests(repo):
    documents = repo["documents"]

    tests = []

    for doc in documents:

        content = doc.get("content", "")

        for line in content.splitlines():

            line = line.strip()

            if line.startswith("def "):

                function_name = (
                    line.replace("def ", "")
                    .split("(")[0]
                )

                tests.append({
                    "function": function_name,
                    "test":
                        f"Create unit tests for {function_name}"
                })

    return {
        "agent": "tester",
        "tests": tests[:50]
    }