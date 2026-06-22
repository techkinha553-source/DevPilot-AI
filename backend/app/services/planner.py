

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


# Backward compatibility for older imports
# app.api.agents expects route_task()
def route_task(task: str) -> str:
    return create_plan(task)
