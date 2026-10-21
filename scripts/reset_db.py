"""
SSI — Reset Database
Drops the SQLite DB, recreates the schema, and reseeds from CSVs.
Run:  python scripts/reset_db.py
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from config import settings


def main():
    db_path = Path(settings.DATABASE_URL.replace("sqlite:///", ""))

    if db_path.exists():
        db_path.unlink()
        print(f"🗑️  Deleted: {db_path}")
    else:
        print(f"ℹ️  No DB found at: {db_path}")

    # Import after deletion so SQLAlchemy creates a fresh file
    from database import Base, engine, SessionLocal, seed_database

    print("→ Creating tables...")
    Base.metadata.create_all(bind=engine)

    print("→ Seeding data...")
    seed_database()

    db = SessionLocal()
    try:
        from models.student import Student
        from models.attendance import Attendance
        print(f"✅ Students   : {db.query(Student).count()}")
        print(f"✅ Attendance : {db.query(Attendance).count()}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
