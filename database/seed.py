"""
SSI — Database Seeder
Loads synthetic CSVs into SQLite (idempotent).
Run standalone:  python database/seed.py
"""

import sys
from pathlib import Path

# Allow imports from project root (backend/, database/, etc.)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

import pandas as pd

from database import Base, engine, SessionLocal, seed_database


def main():
    print("→ Creating tables...")
    Base.metadata.create_all(bind=engine)

    print("→ Seeding data from CSVs...")
    seed_database()

    db = SessionLocal()
    try:
        from models.student import Student
        from models.attendance import Attendance
        n_students = db.query(Student).count()
        n_attendance = db.query(Attendance).count()
        print(f"✅ Students   : {n_students}")
        print(f"✅ Attendance : {n_attendance}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
