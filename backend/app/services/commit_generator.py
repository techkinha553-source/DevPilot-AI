def generate_commit_message(changes):

    changes = changes.lower()
    if "security" in changes:
        return "fix: improve security checks"
    if "test" in changes:
        return "test: add unit tests"
    if "api" in changes:
        return "feat: add new api endpoint"
    return "chore: update project"
