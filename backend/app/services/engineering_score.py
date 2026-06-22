def calculate_engineering_score(repo):

    documents = repo["documents"]
    security = 100
    testing = 50
    documentation = 50
    maintainability = 100
    architecture = 80
    paths = [
        doc.get("path", "").lower()
        for doc in documents
    ]
    # Documentation
    if any("readme" in p for p in paths):
        documentation += 30
    if any("docs" in p for p in paths):
        documentation += 20
    # Testing
    if any("test" in p for p in paths):
        testing += 40
    # Security
    for doc in documents:
        content = doc.get("content", "")
        if "password=" in content.lower():
            security -= 20
        if "api_key" in content.lower():
            security -= 20
        if "secret=" in content.lower():
            security -= 20
        if "except:" in content:
            maintainability -= 5
        if len(content.splitlines()) > 500:
            maintainability -= 5
    security = max(0, min(100, security))
    testing = max(0, min(100, testing))
    documentation = max(0, min(100, documentation))
    maintainability = max(0, min(100, maintainability))
    architecture = max(0, min(100, architecture))
    overall = round(
        (
            security +
            testing +
            documentation +
            maintainability +
            architecture
        ) / 5
    )
    return {
        "security": security,
        "testing": testing,
        "documentation": documentation,
        "maintainability": maintainability,
        "architecture": architecture,
        "overall": overall
    }