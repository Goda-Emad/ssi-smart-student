"""
SSI — Academic Schemas
"""

from pydantic import BaseModel, ConfigDict


class AcademicResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: int
    gpa: float
    total_credits: int
    credits_completed: int
    failed_courses_count: int
    current_semester: int
