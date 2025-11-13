import os
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from .database import engine
from .models import Task, Notification
from sqlmodel import Session, select
from datetime import datetime, timezone
from dateutil import parser

IST = pytz.timezone("Asia/Kolkata")

scheduler = BackgroundScheduler(timezone=timezone.utc)

def check_and_schedule_reminders():
    with Session(engine) as s:
        statement = select(Task).where(Task.reminders_enabled == True)
        tasks = s.exec(statement).all()
        for t in tasks:
            # reminder_times stored as list of ISO strings or datetimes in UTC
            if not t.reminder_times:
                continue
            for rt in t.reminder_times:
                # ensure datetime
                if isinstance(rt, str):
                    dt = parser.isoparse(rt)
                else:
                    dt = rt
                # schedule only future reminders
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                if dt > datetime.now(timezone.utc):
                    job_id = f"reminder_task_{t.id}_{int(dt.timestamp())}"
                    if not scheduler.get_job(job_id):
                        scheduler.add_job(
                            func=send_reminder,
                            trigger="date",
                            run_date=dt,
                            args=[t.id],
                            id=job_id,
                            replace_existing=True
                        )

def send_reminder(task_id: int):
    with Session(engine) as s:
        task = s.get(Task, task_id)
        if not task:
            return
        # create notification for assignee user (if available)
        if task.assignee_employee_id:
            # find user for employee
            from .models import EmployeeProfile, User
            emp = s.get(EmployeeProfile, task.assignee_employee_id)
            if emp and emp.user_id:
                notif = Notification(
                    user_id=emp.user_id,
                    message=f"Reminder: Task '{task.title}' is due {task.due_date} (IST)",
                    data={"task_id": task.id}
                )
                s.add(notif)
                s.commit()
                print(f"[scheduler] Reminder created for user {emp.user_id} about task {task.id}")
        # also create notification for task creator
        if task.created_by_user_id:
            notif = Notification(
                user_id=task.created_by_user_id,
                message=f"Reminder sent for task '{task.title}' (assignee id {task.assignee_employee_id})",
                data={"task_id": task.id}
            )
            s.add(notif)
            s.commit()

def start_scheduler():
    scheduler.start()
    # check the DB and schedule items every minute to pick up new reminders
    scheduler.add_job(check_and_schedule_reminders, "interval", seconds=60, id="sweep_reminders")
