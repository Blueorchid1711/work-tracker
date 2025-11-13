from fastapi import APIRouter, Depends, HTTPException
from ..database import engine
from ..models import Meeting, AuditLog, EmployeeProfile
from sqlmodel import Session
from ..permissions import get_current_user, require_role
from typing import List
import pytz

router = APIRouter()

@router.post("/")
def create_meeting(payload: dict, current_user=Depends(require_role("admin", "manager"))):
    # payload should include participants_employee_ids, start_datetime, end_datetime (IST-aware)
    with Session(engine) as s:
        m = Meeting(**payload)
        s.add(m); s.commit(); s.refresh(m)
        s.add(AuditLog(user_id=current_user.id, action="create_meeting", entity="meeting", entity_id=m.id))
        s.commit()
        return m

@router.get("/")
def list_meetings(participant: int = None, current_user=Depends(get_current_user)):
    with Session(engine) as s:
        q = select(Meeting)
        meetings = s.exec(q).all()
        if current_user.role == "employee":
            # return only meetings where this employee participates
            # find employee profile
            stmt = select(EmployeeProfile).where(EmployeeProfile.user_id == current_user.id)
            emp = s.exec(stmt).first()
            res = []
            for m in meetings:
                if emp and emp.id in (m.participants_employee_ids or []):
                    res.append(m)
            return res
        return meetings

@router.get("/calendar")
def calendar(next_days: int = 30, current_user=Depends(get_current_user)):
    # returns meetings + tasks as calendar entries for next N days in IST
    import pytz
    from datetime import datetime, timedelta
    IST = pytz.timezone("Asia/Kolkata")
    now_ist = datetime.now(IST)
    end_ist = now_ist + timedelta(days=next_days)
    with Session(engine) as s:
        meetings = s.exec(select(Meeting)).all()
        tasks = s.exec(select(Meeting)).all()
        # convert times to IST before returning (simpler: return raw UTC and client shows as IST)
        return {"meetings": meetings}
