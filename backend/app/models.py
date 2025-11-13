from sqlmodel import SQLModel, Field, Relationship, JSON
from typing import Optional, List
from datetime import datetime
import uuid

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    role: str = Field(default="employee")  # admin|manager|employee
    full_name: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.utcnow())

class EmployeeProfile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", index=True, nullable=True)
    role: Optional[str] = None
    joined_at: datetime = Field(default_factory=lambda: datetime.utcnow())
    bio: Optional[str] = None
    # allow extensible profile fields
    profile_data: Optional[dict] = Field(default_factory=dict, sa_column_kwargs={"type_": JSON})

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    assignee_employee_id: Optional[int] = Field(default=None, foreign_key="employeeprofile.id", index=True)
    created_by_user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    status: str = Field(default="todo")  # todo,in_progress,done
    due_date: Optional[datetime] = None  # timezone-aware stored in UTC
    reminders_enabled: bool = Field(default=False)
    reminder_times: Optional[List[datetime]] = Field(default_factory=list, sa_column_kwargs={"type_": JSON})
    created_at: datetime = Field(default_factory=lambda: datetime.utcnow())
    completed_at: Optional[datetime] = None

class FileMeta(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    content_type: Optional[str]
    uploader_user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    linked_employee_id: Optional[int] = Field(default=None, foreign_key="employeeprofile.id")
    linked_task_id: Optional[int] = Field(default=None, foreign_key="task.id")
    saved_path_or_s3_key: str
    created_at: datetime = Field(default_factory=lambda: datetime.utcnow())

class Meeting(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    organizer_user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    participants_employee_ids: Optional[List[int]] = Field(default_factory=list, sa_column_kwargs={"type_": JSON})
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None
    location_or_zoom: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.utcnow())

class Commit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: Optional[int] = Field(default=None, foreign_key="employeeprofile.id")
    repo: Optional[str] = None
    commit_sha: Optional[str] = None
    commit_date: Optional[datetime] = None
    message: Optional[str] = None

class Notification(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    message: str
    data: Optional[dict] = Field(default_factory=dict, sa_column_kwargs={"type_": JSON})
    read: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.utcnow())

class AuditLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    action: str
    entity: Optional[str] = None
    entity_id: Optional[int] = None
    details: Optional[dict] = Field(default_factory=dict, sa_column_kwargs={"type_": JSON})
    created_at: datetime = Field(default_factory=lambda: datetime.utcnow())
