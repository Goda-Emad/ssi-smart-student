"""
SSI — Database Models
"""

from models.student import Student
from models.academic_record import AcademicRecord
from models.attendance import Attendance
from models.risk_score import RiskScore

__all__ = ["Student", "AcademicRecord", "Attendance", "RiskScore"]
