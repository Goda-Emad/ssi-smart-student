"""
SSI — Attendance Router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas.attendance import AttendanceResponse
from services.attendance_service import get_attendance_by_student_id

router = APIRouter()


@router.get("/{student_id}", response_model=list[AttendanceResponse])
def get_attendance(student_id: str, db: Session = Depends(get_db)):
    records = get_attendance_by_student_id(db, student_id)
    if not records:
        raise HTTPException(status_code=404, detail="No attendance records found")
    return records
