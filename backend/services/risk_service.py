"""
SSI — Risk Service
"""

from sqlalchemy.orm import Session

from models.student import Student
from models.risk_score import RiskScore
from ai.risk_model import get_risk_model


def _student_to_features(student: Student) -> dict:
    return {
        "gender": student.gender,
        "age": student.age,
        "faculty": student.faculty,
        "department": student.department,
        "academic_year": student.academic_year,
        "enrollment_type": student.enrollment_type,
        "admission_score": student.admission_score,
        "gpa": student.gpa,
        "total_credits": student.total_credits,
        "credits_completed": student.credits_completed,
        "failed_courses_count": student.failed_courses_count,
        "current_semester": student.current_semester,
        "attendance_rate": student.attendance_rate,
        "absence_days": student.absence_days,
        "late_submissions": student.late_submissions,
        "library_visits": student.library_visits,
        "lms_logins": student.lms_logins,
        "extracurricular": student.extracurricular,
        "disciplinary_actions": student.disciplinary_actions,
        "tuition_status": student.tuition_status,
        "financial_aid": student.financial_aid,
        "previous_warnings": student.previous_warnings,
        "advisor_meetings": student.advisor_meetings,
        "stress_level": student.stress_level,
        "part_time_job": student.part_time_job,
        "commute_distance_km": student.commute_distance_km,
    }


def predict_student_risk(db: Session, student_id: str):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        return None

    model = get_risk_model()
    result = model.predict(_student_to_features(student))

    risk_label = int(result["risk_label"][0])
    risk_score = float(result["risk_score"][0])
    risk_level = result["risk_level"][0]

    # Persist
    db.add(RiskScore(
        student_id=student.id,
        risk_label=risk_label,
        risk_score=risk_score,
        risk_level=risk_level,
    ))
    db.commit()

    return {
        "student_id": student.student_id,
        "risk_label": risk_label,
        "risk_score": risk_score,
        "risk_level": risk_level,
    }


def get_at_risk_students(db: Session):
    students = db.query(Student).filter(Student.risk_label == 1).all()
    model = get_risk_model()

    results = []
    for s in students:
        r = model.predict(_student_to_features(s))
        results.append({
            "student_id": s.student_id,
            "full_name": s.full_name,
            "faculty": s.faculty,
            "gpa": s.gpa,
            "attendance_rate": s.attendance_rate,
            "risk_score": float(r["risk_score"][0]),
            "risk_level": r["risk_level"][0],
        })
    results.sort(key=lambda x: x["risk_score"], reverse=True)
    return results
