from fastapi import APIRouter, Depends
from ..database import engine
from ..models import Task, Notification
from sqlmodel import Session, select
from ..permissions import get_current_user

router = APIRouter()

@router.get("/pending")
def pending_reminders(current_user=Depends(get_current_user)):
    # returns notifications for user not read
    with Session(engine) as s:
        q = select(Notification).where(Notification.user_id == current_user.id, Notification.read == False)
        notifs = s.exec(q).all()
        return notifs
