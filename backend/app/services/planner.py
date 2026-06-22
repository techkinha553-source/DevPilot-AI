from app.services.openai_service import get_client

client = get_client()

def create_plan(task: str) -> str:
    q = task.lower()

    if any(word in q for word in [
        "security",
        "vulnerability",
        "secret",
        "password",
        "token"
    ]):
        return "security"

    if any(word in q for word in [
        "architecture",
        "design",
        "structure"
    ]):
        return "architect"

    if any(word in q for word in [
        "bug",
        "review",
        "smell",
        "quality",
        "refactor"
    ]):
        return "reviewer"

    if any(word in q for word in [
        "test",
        "testing",
        "unit test"
    ]):
        return "tester"

    return "assistant"
