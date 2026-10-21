"""
SSI — Services Package
"""

from services.student_service import get_student_by_student_id
from services.academic_service import get_academic_by_student_id
from services.attendance_service import get_attendance_by_student_id
from services.risk_service import predict_student_risk, get_at_risk_students
from services.dashboard_service import get_summary

__all__ = [
    "get_student_by_student_id",
    "get_academic_by_student_id",
    "get_attendance_by_student_id",
    "predict_student_risk",
    "get_at_risk_students",
    "get_summary",
]
