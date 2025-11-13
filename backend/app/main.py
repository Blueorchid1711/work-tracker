from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from .database import init_db, engine
from .scheduler import start_scheduler
from . import seed
from .routes import users, employees, tasks, uploads, meetings, reminders, dashboard, webhooks
from .models import *
from sqlmodel import Session, select

app = FastAPI(title="Employee Work Tracker")

# CORS for frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()
    # run seed if empty
    seed.seed_if_needed()
    # start scheduler
    start_scheduler()

# include routers
app.include_router(users.router, prefix="/api/auth")
app.include_router(users.router_users, prefix="/api/users")
app.include_router(employees.router, prefix="/api/employees")
app.include_router(tasks.router, prefix="/api/tasks")
app.include_router(uploads.router, prefix="/api/upload")
app.include_router(meetings.router, prefix="/api/meetings")
app.include_router(reminders.router, prefix="/api/reminders")
app.include_router(dashboard.router, prefix="/api")
app.include_router(webhooks.router, prefix="/webhook")
