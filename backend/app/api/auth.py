from fastapi import APIRouter, HTTPException

from app.models.user import UserSignup, UserLogin
from app.services.user_store import users
from app.services.user_store import users, user_stats

router = APIRouter()

@router.post("/signup")
def signup(user: UserSignup):

    if user.email in users:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    users[user.email] = {
        "email": user.email,
        "password": user.password
    }

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

    return {
        "message": "Login successful",
        "email": user.email
    }
