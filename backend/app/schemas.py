from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    email: str
    role: str
    full_name: Optional[str]

class TaskCreate(BaseModel):
    title: str
    description: Optional[str]
    assignee_employee_id: Optional[int]
    due_date: Optional[datetime]
    reminders_enabled: Optional[bool] = False
    reminder_times: Optional[List[datetime]] = []
