"""
SSI — AcademicRecord Model
"""

from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class AcademicRecord(Base):
    __tablename__ = "academic_records"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(
        Integer,
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    gpa = Column(Float, nullable=False, default=0.0)
    total_credits = Column(Integer, nullable=False, default=0)
    credits_completed = Column(Integer, nullable=False, default=0)
    failed_courses_count = Column(Integer, nullable=False, default=0)
    current_semester = Column(Integer, nullable=False, default=1)

    student = relationship("Student", back_populates="academic_record")
