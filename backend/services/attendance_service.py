"""
SSI — Attendance Service
"""

from sqlalchemy.orm import Session

from models.student import Student
from models.attendance import Attendance


def get_attendance_by_student_id(db: Session, student_id: str):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        return None
    return (
        db.query(Attendance)
        .filter(Attendance.student_id == student.id)
        .order_by(Attendance.session_date.desc())
        .all()
    )
