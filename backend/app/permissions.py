from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from .models import User, EmployeeProfile
from .database import engine, get_session
from sqlmodel import Session, select
from .auth import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid auth token")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    with Session(engine) as s:
        user = s.get(User, int(user_id))
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user

def require_role(*roles):
    def _checker(user: User = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return _checker

def visibility_employee(employee: EmployeeProfile, current_user: User):
    # employees cannot see admin users' profiles (owner admin)
    if employee.user_id:
        with Session(engine) as s:
            user = s.get(User, employee.user_id)
            if user and user.role == "admin" and current_user.role == "employee":
                raise HTTPException(status_code=403, detail="Forbidden")
    return True
