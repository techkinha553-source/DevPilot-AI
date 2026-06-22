def generate_test_cases(documents):

    tests = []

    for doc in documents:

        path = doc.get("path", "")

        content = doc.get("content", "")

        if ".py" not in path:
            continue

        for line in content.splitlines():

            line = line.strip()

            if line.startswith("def "):

                function_name = (
                    line.replace("def ", "")
                    .split("(")[0]
                )

                tests.append({
                    "function": function_name,
                    "suggested_test":
                        f"Test {function_name} with valid input, invalid input, and edge cases."
                })

    return tests
