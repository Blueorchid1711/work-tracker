from fastapi import APIRouter, Depends, HTTPException
from ..permissions import get_current_user, require_role, visibility_employee
from ..database import engine
from sqlmodel import Session, select
from ..models import EmployeeProfile, User, AuditLog
from typing import List

router = APIRouter()

@router.post("/")
def create_employee(payload: dict, current_user: User = Depends(require_role("admin"))):
    with Session(engine) as s:
        emp = EmployeeProfile(**payload)
        s.add(emp); s.commit(); s.refresh(emp)
        s.add(AuditLog(user_id=current_user.id, action="create_employee", entity="employee", entity_id=emp.id))
        s.commit()
        return emp

@router.get("/", response_model=List[EmployeeProfile])
def list_employees(current_user: User = Depends(get_current_user)):
    with Session(engine) as s:
        stmt = select(EmployeeProfile)
        emps = s.exec(stmt).all()
        # employees cannot see admin user profiles
        if current_user.role == "employee":
            filtered = []
            for e in emps:
                if e.user_id:
                    user = s.get(User, e.user_id)
                    if user and user.role == "admin":
                        continue
                filtered.append(e)
            return filtered
        return emps

@router.get("/{id}")
def get_employee(id: int, current_user: User = Depends(get_current_user)):
    with Session(engine) as s:
        emp = s.get(EmployeeProfile, id)
        if not emp:
            raise HTTPException(status_code=404, detail="Not found")
        if current_user.role == "employee":
            if emp.user_id:
                user = s.get(User, emp.user_id)
                if user and user.role == "admin":
                    raise HTTPException(status_code=403, detail="Forbidden")
        return emp

@router.put("/{id}")
def update_employee(id: int, data: dict, current_user: User = Depends(get_current_user)):
    # admin can edit; manager may edit limited fields (here: bio)
    with Session(engine) as s:
        emp = s.get(EmployeeProfile, id)
        if not emp:
            raise HTTPException(status_code=404)
        if current_user.role == "manager":
            # manager edit limited
            allowed = {"bio", "profile_data"}
            for k in list(data.keys()):
                if k not in allowed:
                    data.pop(k, None)
        elif current_user.role != "admin":
            raise HTTPException(status_code=403)
        for k, v in data.items():
            setattr(emp, k, v)
        s.add(emp); s.commit()
        s.add(AuditLog(user_id=current_user.id, action="update_employee", entity="employee", entity_id=emp.id))
        s.commit()
        return emp
