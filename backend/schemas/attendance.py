"""
SSI — Attendance Schemas
"""

from datetime import date
from pydantic import BaseModel, ConfigDict


class AttendanceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    record_id: str
    student_id: int
    course_code: str
    course_name: str
    semester: int
    session_date: date
    session_type: str
    status: str
    duration_minutes: int
