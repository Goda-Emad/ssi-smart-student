"""
SSI — Attendance Model
"""

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    record_id = Column(String(20), unique=True, nullable=False, index=True)
    student_id = Column(
        Integer,
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    course_code = Column(String(20), nullable=False)
    course_name = Column(String(150), nullable=False)
    semester = Column(Integer, nullable=False)
    session_date = Column(Date, nullable=False)
    session_type = Column(String(20), nullable=False)  # Lecture / Lab / Tutorial
    status = Column(String(20), nullable=False)        # Present / Absent / Late / Excused
    duration_minutes = Column(Integer, nullable=False, default=0)

    student = relationship("Student", back_populates="attendance_records")
