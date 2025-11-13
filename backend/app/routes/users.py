from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas import Token, UserCreate, UserRead
from ..auth import create_access_token, get_password_hash, verify_password
from ..database import engine
from ..models import User, AuditLog
from sqlmodel import Session, select
from ..permissions import get_current_user, require_role

router = APIRouter()

@router.post("/register", response_model=UserRead)
def register(user_in: UserCreate):
    with Session(engine) as s:
        statement = select(User).where((User.username == user_in.username) | (User.email == user_in.email))
        existing = s.exec(statement).first()
        if existing:
            raise HTTPException(status_code=400, detail="User exists")
        user = User(username=user_in.username, email=user_in.email, hashed_password=get_password_hash(user_in.password), role="employee")
        s.add(user); s.commit(); s.refresh(user)
        return UserRead.from_orm(user)

@router.post("/login", response_model=Token)
def login(form: UserCreate):
    # Using same schema for simplicity (username/email + password)
    with Session(engine) as s:
        statement = select(User).where((User.username == form.username) | (User.email == form.username))
        user = s.exec(statement).first()
        if not user or not verify_password(form.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = create_access_token({"sub": str(user.id), "role": user.role})
        return {"access_token": token}

# separate router for users endpoints (profile)
router_users = APIRouter()

@router_users.get("/me", response_model=UserRead)
def read_me(current_user: User = Depends(get_current_user)):
    return UserRead.from_orm(current_user)

@router_users.put("/me")
def update_me(data: dict, current_user: User = Depends(get_current_user)):
    with Session(engine) as s:
        user = s.get(User, current_user.id)
        if "full_name" in data:
            user.full_name = data["full_name"]
        if "email" in data:
            user.email = data["email"]
        if "password" in data:
            user.hashed_password = get_password_hash(data["password"])
        s.add(user); s.commit()
        # audit
        s.add(AuditLog(user_id=user.id, action="update_profile", entity="user", entity_id=user.id))
        s.commit()
        return {"status":"ok"}
