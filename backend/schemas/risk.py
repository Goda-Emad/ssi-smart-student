"""
SSI — Risk Schemas
"""

from pydantic import BaseModel


class RiskResponse(BaseModel):
    student_id: str
    risk_label: int
    risk_score: float
    risk_level: str


class AtRiskStudent(BaseModel):
    student_id: str
    full_name: str
    faculty: str
    gpa: float
    attendance_rate: float
    risk_score: float
    risk_level: str
