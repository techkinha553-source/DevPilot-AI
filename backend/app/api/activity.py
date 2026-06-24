from fastapi import APIRouter
from app.services.activity_store import activity_log

router = APIRouter()

@router.get("/activity")
def get_activity():

    return activity_log[-20:]