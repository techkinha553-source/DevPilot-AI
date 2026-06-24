import json


def analyze_dependencies(repo):

    documents = repo["documents"]

    python_dependencies = []
    javascript_dependencies = []

    warnings = []

    for doc in documents:

        path = doc.get(
            "path",
            ""
        ).lower()

        content = doc.get(
            "content",
            ""
        )

        if path.endswith(
            "requirements.txt"
        ):

            for line in content.splitlines():

                line = line.strip()

                if (
                    line
                    and
                    not line.startswith("#")
                ):
                    python_dependencies.append(
                        line
                    )

        elif path.endswith(
            "package.json"
        ):

            try:

                package_data = json.loads(
                    content
                )

                deps = package_data.get(
                    "dependencies",
                    {}
                )

                javascript_dependencies.extend(
                    deps.keys()
                )

            except Exception:
                warnings.append(
                    "Failed to parse package.json"
                )

    total_dependencies = (
        len(python_dependencies)
        +
        len(javascript_dependencies)
    )

    if total_dependencies > 50:

        warnings.append(
            "Large dependency count detected"
        )

    return {
        "dependency_files":
            len(
                python_dependencies
            )
            +
            len(
                javascript_dependencies
            ),
        "python_dependencies":
            python_dependencies,
        "javascript_dependencies":
            javascript_dependencies,
        "warnings":
            warnings
    }