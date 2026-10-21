"""
SSI — Dashboard Service
"""

from sqlalchemy import func
from sqlalchemy.orm import Session

from models.student import Student


def get_summary(db: Session) -> dict:
    total = db.query(func.count(Student.id)).scalar() or 0
    at_risk = db.query(func.count(Student.id)).filter(Student.risk_label == 1).scalar() or 0
    avg_gpa = db.query(func.avg(Student.gpa)).scalar() or 0.0
    avg_attendance = db.query(func.avg(Student.attendance_rate)).scalar() or 0.0

    by_faculty = (
        db.query(Student.faculty, func.count(Student.id))
        .group_by(Student.faculty)
        .all()
    )

    return {
        "total_students": total,
        "at_risk_students": at_risk,
        "at_risk_percentage": round((at_risk / total) * 100, 2) if total else 0.0,
        "average_gpa": round(float(avg_gpa), 2),
        "average_attendance": round(float(avg_attendance), 2),
        "students_by_faculty": [{"faculty": f, "count": c} for f, c in by_faculty],
    }
