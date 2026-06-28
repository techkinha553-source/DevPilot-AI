from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
import os
import requests

from app.models.user import UserSignup, UserLogin
from app.services.user_store import users, user_stats
from app.services.user_store import save_users

router = APIRouter()

# Placeholder GitHub OAuth configuration.
# Replace these values with real OAuth credentials in a later phase.
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID", "YOUR_GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET", "YOUR_GITHUB_CLIENT_SECRET")
GITHUB_CALLBACK_URL = "http://localhost:8000/auth/github/callback"

@router.post("/signup")
def signup(user: UserSignup):

    if user.email in users:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    print("BEFORE:", users)

    users[user.email] = {
        "email": user.email,
        "password": user.password
    }

    save_users()

    print("AFTER:", users)

    user_stats[user.email] = {
        "repositories": 0,
        "files_analyzed": 0,
        "questions_asked": 0,
        "avg_health_score": 0
    }  

    return {
        "message": "Signup successful"
    }


@router.post("/login")
def login(user: UserLogin):

    existing = users.get(user.email)

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if existing["password"] != user.password:
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    print("LOGIN USERS:", users)
    print("LOGIN EMAIL:", user.email)

    return {
        "message": "Login successful",
        "email": user.email
    }


# --- GitHub OAuth endpoints ---
@router.get("/auth/github")
def github_login():
    github_url = (
        "https://github.com/login/oauth/authorize"
        f"?client_id={GITHUB_CLIENT_ID}"
        f"&redirect_uri={GITHUB_CALLBACK_URL}"
        "&scope=repo,user"
    )

    return RedirectResponse(github_url)


@router.get("/auth/github/callback")
def github_callback(code: str | None = None):
    if not code:
        raise HTTPException(
            status_code=400,
            detail="GitHub authorization code not received."
        )

    token_response = requests.post(
        "https://github.com/login/oauth/access_token",
        headers={"Accept": "application/json"},
        data={
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code,
            "redirect_uri": GITHUB_CALLBACK_URL,
        },
        timeout=15,
    )

    token_data = token_response.json()

    if "access_token" not in token_data:
        raise HTTPException(
            status_code=400,
            detail="Failed to obtain GitHub access token."
        )

    access_token = token_data["access_token"]

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github+json",
    }

    profile_response = requests.get(
        "https://api.github.com/user",
        headers=headers,
        timeout=15,
    )

    profile = profile_response.json()

    repos_response = requests.get(
        "https://api.github.com/user/repos?per_page=100&sort=updated",
        headers=headers,
        timeout=15,
    )

    repos_json = repos_response.json()

    repositories = []
    if isinstance(repos_json, list):
        repositories = [repo.get("name", "") for repo in repos_json]

    from urllib.parse import urlencode

    params = urlencode({
        "connected": "true",
        "username": profile.get("login", ""),
        "avatar_url": profile.get("avatar_url", ""),
        "repositories": ",".join(repositories),
    })

    frontend_url = f"http://localhost:3000/chat?{params}"

    return RedirectResponse(frontend_url)
