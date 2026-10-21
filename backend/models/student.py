"""
SSI — Student Model
"""

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(String(20), unique=True, nullable=False, index=True)
    full_name = Column(String(150), nullable=False)
    gender = Column(String(10), nullable=False)
    age = Column(Integer, nullable=False)
    faculty = Column(String(100), nullable=False)
    department = Column(String(100), nullable=False)
    academic_year = Column(Integer, nullable=False)
    enrollment_type = Column(String(30), nullable=False)
    admission_score = Column(Float, nullable=False)

    gpa = Column(Float, nullable=False, default=0.0)
    total_credits = Column(Integer, nullable=False, default=0)
    credits_completed = Column(Integer, nullable=False, default=0)
    failed_courses_count = Column(Integer, nullable=False, default=0)
    current_semester = Column(Integer, nullable=False, default=1)

    attendance_rate = Column(Float, nullable=False, default=0.0)
    absence_days = Column(Integer, nullable=False, default=0)
    late_submissions = Column(Integer, nullable=False, default=0)
    library_visits = Column(Integer, nullable=False, default=0)
    lms_logins = Column(Integer, nullable=False, default=0)

    extracurricular = Column(String(5), nullable=False, default="No")
    disciplinary_actions = Column(Integer, nullable=False, default=0)
    tuition_status = Column(String(20), nullable=False, default="Paid")
    financial_aid = Column(String(5), nullable=False, default="No")
    previous_warnings = Column(Integer, nullable=False, default=0)
    advisor_meetings = Column(Integer, nullable=False, default=0)
    stress_level = Column(Integer, nullable=False, default=0)
    part_time_job = Column(String(5), nullable=False, default="No")
    commute_distance_km = Column(Float, nullable=False, default=0.0)

    risk_label = Column(Integer, nullable=False, default=0)

    academic_record = relationship(
        "AcademicRecord", back_populates="student", uselist=False, cascade="all, delete-orphan"
    )
    attendance_records = relationship(
        "Attendance", back_populates="student", cascade="all, delete-orphan"
    )
    risk_scores = relationship(
        "RiskScore", back_populates="student", cascade="all, delete-orphan"
    )
