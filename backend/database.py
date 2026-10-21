"""
SSI — Database
SQLAlchemy engine, session, and CSV seeder.
"""

from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from config import settings


# ---------- Engine & Session ----------
Path(settings.DATABASE_URL.replace("sqlite:///", "")).parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {},
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ---------- Dependency ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- Seeder ----------
def seed_database():
    """
    Load synthetic CSVs into the database (idempotent).
    Called once at app startup.
    """
    from models.student import Student
    from models.academic_record import AcademicRecord
    from models.attendance import Attendance

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if db.query(Student).first() is not None:
            return  # already seeded

        # --- Students ---
        if settings.STUDENTS_CSV.exists():
            students_df = pd.read_csv(settings.STUDENTS_CSV)
            for _, row in students_df.iterrows():
                student = Student(
                    student_id=row["student_id"],
                    full_name=row["full_name"],
                    gender=row["gender"],
                    age=int(row["age"]),
                    faculty=row["faculty"],
                    department=row["department"],
                    academic_year=int(row["academic_year"]),
                    enrollment_type=row["enrollment_type"],
                    admission_score=float(row["admission_score"]),
                    gpa=float(row["gpa"]),
                    total_credits=int(row["total_credits"]),
                    credits_completed=int(row["credits_completed"]),
                    failed_courses_count=int(row["failed_courses_count"]),
                    current_semester=int(row["current_semester"]),
                    attendance_rate=float(row["attendance_rate"]),
                    absence_days=int(row["absence_days"]),
                    late_submissions=int(row["late_submissions"]),
                    library_visits=int(row["library_visits"]),
                    lms_logins=int(row["lms_logins"]),
                    extracurricular=row["extracurricular"],
                    disciplinary_actions=int(row["disciplinary_actions"]),
                    tuition_status=row["tuition_status"],
                    financial_aid=row["financial_aid"],
                    previous_warnings=int(row["previous_warnings"]),
                    advisor_meetings=int(row["advisor_meetings"]),
                    stress_level=int(row["stress_level"]),
                    part_time_job=row["part_time_job"],
                    commute_distance_km=float(row["commute_distance_km"]),
                    risk_label=int(row["risk_label"]),
                )
                db.add(student)

                academic = AcademicRecord(
                    student_id=row["student_id"],
                    gpa=float(row["gpa"]),
                    total_credits=int(row["total_credits"]),
                    credits_completed=int(row["credits_completed"]),
                    failed_courses_count=int(row["failed_courses_count"]),
                    current_semester=int(row["current_semester"]),
                )
                db.add(academic)
            db.commit()

        # --- Attendance ---
        if settings.ATTENDANCE_CSV.exists():
            att_df = pd.read_csv(settings.ATTENDANCE_CSV)
            batch = []
            for _, row in att_df.iterrows():
                batch.append(Attendance(
                    record_id=row["record_id"],
                    student_id=row["student_id"],
                    course_code=row["course_code"],
                    course_name=row["course_name"],
                    semester=int(row["semester"]),
                    session_date=pd.to_datetime(row["session_date"]).date(),
                    session_type=row["session_type"],
                    status=row["status"],
                    duration_minutes=int(row["duration_minutes"]),
                ))
                if len(batch) >= 5000:
                    db.bulk_save_objects(batch)
                    db.commit()
                    batch = []
            if batch:
                db.bulk_save_objects(batch)
                db.commit()

    finally:
        db.close()
