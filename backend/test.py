from app.services.github_service import clone_repository

repo_id, path = clone_repository(
    "https://github.com/octocat/Hello-World.git"
)

print("Repository ID:", repo_id)
print("Path:", path)