from collections import Counter


def generate_architecture_report(repo):

    documents = repo["documents"]

    technologies = []

    frontend = []
    backend = []
    databases = []

    for doc in documents:

        path = doc.get("path", "").lower()
        content = doc.get("content", "").lower()

        # Frontend Detection
        if "react" in content:
            frontend.append("React")

        if "next" in path or "next" in content:
            frontend.append("Next.js")

        # Backend Detection
        if "fastapi" in content:
            backend.append("FastAPI")

        if "flask" in content:
            backend.append("Flask")

        if "django" in content:
            backend.append("Django")

        # Database Detection
        if "mongodb" in content:
            databases.append("MongoDB")

        if "sqlalchemy" in content:
            databases.append("SQL")

        if "postgres" in content:
            databases.append("PostgreSQL")

    frontend = list(set(frontend))
    backend = list(set(backend))
    databases = list(set(databases))

    return {
    "frontend": frontend,
    "backend": backend,
    "database": databases,
    "total_files": len(documents),

    "layers": {
        "api": True,
        "services": True,
        "storage": True,
        "authentication": True
    },

    "architecture_score": 85,

    "recommendations": [
        "Add caching layer",
        "Add unit testing",
        "Add CI/CD pipeline"
    ]
}
