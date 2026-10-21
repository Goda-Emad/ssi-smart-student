"""
SSI — FastAPI Application Entry Point
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from database import seed_database

from routers import (
    auth,
    students,
    academic,
    attendance,
    early_warning,
    dashboard,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure DB is created and seeded
    seed_database()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN, "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Routers ----------
app.include_router(auth.router,           prefix="/api/auth",           tags=["Auth"])
app.include_router(students.router,       prefix="/api/students",       tags=["Students"])
app.include_router(academic.router,       prefix="/api/academic",       tags=["Academic"])
app.include_router(attendance.router,     prefix="/api/attendance",     tags=["Attendance"])
app.include_router(early_warning.router,  prefix="/api/early-warning",  tags=["Early Warning"])
app.include_router(dashboard.router,      prefix="/api/dashboard",      tags=["Dashboard"])


@app.get("/", tags=["Health"])
def health():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
    }
