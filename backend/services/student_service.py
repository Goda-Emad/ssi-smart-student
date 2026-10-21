"""
SSI — Student Service
"""

from sqlalchemy.orm import Session

from models.student import Student


def get_student_by_student_id(db: Session, student_id: str):
    return db.query(Student).filter(Student.student_id == student_id).first()
