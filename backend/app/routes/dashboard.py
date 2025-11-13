from fastapi import APIRouter, Depends, HTTPException
from ..permissions import get_current_user, require_role
from ..database import engine
from ..models import Task, EmployeeProfile, User
from sqlmodel import Session, select
from typing import Dict, Any
from datetime import datetime, timedelta
import pytz

router = APIRouter()

@router.get("/dashboard")
def dashboard(current_user=Depends(get_current_user)):
    with Session(engine) as s:
        total_emps = s.exec(select(EmployeeProfile)).all()
        total_tasks = s.exec(select(Task)).all()
        overdue = [t for t in total_tasks if t.due_date and t.due_date < datetime.utcnow() and t.status != "done"]
        upcoming = [t for t in total_tasks if t.due_date and t.due_date > datetime.utcnow() and (t.due_date - datetime.utcnow()).days <= 7]
        return {
            "total_employees": len(total_emps),
            "total_tasks": len(total_tasks),
            "overdue_tasks": len(overdue),
            "upcoming_deadlines": len(upcoming)
        }

@router.get("/stats/productivity")
def stats_productivity(period: int = 30, current_user=Depends(require_role("admin", "manager"))):
    with Session(engine) as s:
        since = datetime.utcnow() - timedelta(days=period)
        tasks = s.exec(select(Task)).all()
        # per-employee breakdown
        emps = s.exec(select(EmployeeProfile)).all()
        result = []
        for e in emps:
            emp_tasks = [t for t in tasks if t.assignee_employee_id == e.id and t.created_at >= since]
            completed = [t for t in emp_tasks if t.status == "done"]
            on_time = [t for t in completed if t.completed_at and t.due_date and t.completed_at <= t.due_date]
            avg_completion = None
            if completed:
                total = sum(((t.completed_at - t.created_at).total_seconds() for t in completed if t.completed_at), 0.0)
                avg_completion = total / len(completed)
            result.append({
                "employee_id": e.id,
                "tasks_assigned": len(emp_tasks),
                "tasks_completed": len(completed),
                "on_time": len(on_time),
                "avg_completion_seconds": avg_completion
            })
        return {"per_employee": result}
