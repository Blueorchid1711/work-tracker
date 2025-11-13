from .database import engine
from sqlmodel import Session, select
from .models import User, EmployeeProfile, Task, FileMeta, Meeting
from .auth import get_password_hash
from datetime import datetime, timedelta
import pytz

IST = pytz.timezone("Asia/Kolkata")

def seed_if_needed():
    with Session(engine) as s:
        stmt = select(User)
        users = s.exec(stmt).all()
        if users:
            return
        # create admin
        admin = User(username="admin", email="admin@example.com", hashed_password=get_password_hash("adminpass"), role="admin", full_name="Admin Boss")
        manager = User(username="manager", email="manager@example.com", hashed_password=get_password_hash("managerpass"), role="manager", full_name="Team Manager")
        alice = User(username="alice", email="alice@example.com", hashed_password=get_password_hash("alicepass"), role="employee", full_name="Alice Employee")
        bob = User(username="bob", email="bob@example.com", hashed_password=get_password_hash("bobpass"), role="employee", full_name="Bob Employee")
        carol = User(username="carol", email="carol@example.com", hashed_password=get_password_hash("carolpass"), role="employee", full_name="Carol Employee")
        s.add(admin); s.add(manager); s.add(alice); s.add(bob); s.add(carol)
        s.commit()
        # employee profiles
        p1 = EmployeeProfile(user_id=alice.id, role="developer", bio="Works on frontend")
        p2 = EmployeeProfile(user_id=bob.id, role="developer", bio="Works on backend")
        p3 = EmployeeProfile(user_id=carol.id, role="qa", bio="Quality assurance")
        s.add_all([p1, p2, p3]); s.commit()
        # tasks: some overdue, some upcoming
        now_ist = datetime.now(IST)
        overdue = now_ist - timedelta(days=2)
        upcoming1 = now_ist + timedelta(days=3)
        upcoming2 = now_ist + timedelta(days=1, hours=5)
        # convert to UTC to store
        overdue_utc = overdue.astimezone(pytz.utc)
        upcoming1_utc = upcoming1.astimezone(pytz.utc)
        upcoming2_utc = upcoming2.astimezone(pytz.utc)
        t1 = Task(title="Fix critical bug", description="Production bug", assignee_employee_id=p1.id, created_by_user_id=manager.id, status="in_progress", due_date=overdue_utc, reminders_enabled=True, reminder_times=[(overdue_utc - timedelta(hours=24)).isoformat()])
        t2 = Task(title="Write unit tests", description="Cover core modules", assignee_employee_id=p2.id, created_by_user_id=manager.id, status="todo", due_date=upcoming1_utc, reminders_enabled=True, reminder_times=[(upcoming1_utc - timedelta(hours=24)).isoformat(), (upcoming1_utc - timedelta(hours=1)).isoformat()])
        t3 = Task(title="Prepare release notes", description="", assignee_employee_id=p3.id, created_by_user_id=manager.id, status="todo", due_date=upcoming2_utc, reminders_enabled=False)
        s.add_all([t1, t2, t3]); s.commit()
        # meetings next 30 days
        m1_start = (now_ist + timedelta(days=2)).replace(hour=10, minute=0)
        m1_end = m1_start + timedelta(hours=1)
        m1 = Meeting(title="Sprint Planning", description="Plan sprint", organizer_user_id=manager.id, participants_employee_ids=[p1.id, p2.id, p3.id], start_datetime=m1_start.astimezone(pytz.utc), end_datetime=m1_end.astimezone(pytz.utc), location_or_zoom="Zoom")
        s.add(m1); s.commit()
        print("Database seeded with admin/manager/employees, tasks, meetings")
