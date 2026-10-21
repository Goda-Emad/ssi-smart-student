"""
SSI — Academic Service
"""

from sqlalchemy.orm import Session

from models.student import Student
from models.academic_record import AcademicRecord


def get_academic_by_student_id(db: Session, student_id: str):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        return None
    return (
        db.query(AcademicRecord)
        .filter(AcademicRecord.student_id == student.id)
        .first()
    )
