"""
SSI — Student Schemas
"""

from pydantic import BaseModel, ConfigDict


class StudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: str
    full_name: str
    gender: str
    age: int
    faculty: str
    department: str
    academic_year: int
    enrollment_type: str
    admission_score: float
    gpa: float
    total_credits: int
    credits_completed: int
    failed_courses_count: int
    current_semester: int
    attendance_rate: float
    absence_days: int
    late_submissions: int
    library_visits: int
    lms_logins: int
    extracurricular: str
    disciplinary_actions: int
    tuition_status: str
    financial_aid: str
    previous_warnings: int
    advisor_meetings: int
    stress_level: int
    part_time_job: str
    commute_distance_km: float
    risk_label: int
