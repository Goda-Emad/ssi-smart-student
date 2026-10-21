"""
SSI — Pydantic Schemas
"""

from schemas.student import StudentResponse
from schemas.academic import AcademicResponse
from schemas.attendance import AttendanceResponse
from schemas.auth import LoginRequest, TokenResponse
from schemas.risk import RiskResponse, AtRiskStudent

__all__ = [
    "StudentResponse",
    "AcademicResponse",
    "AttendanceResponse",
    "LoginRequest",
    "TokenResponse",
    "RiskResponse",
    "AtRiskStudent",
]
