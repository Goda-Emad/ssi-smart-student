"""
SSI — Academic Router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas.academic import AcademicResponse
from services.academic_service import get_academic_by_student_id

router = APIRouter()


@router.get("/{student_id}", response_model=AcademicResponse)
def get_academic(student_id: str, db: Session = Depends(get_db)):
    record = get_academic_by_student_id(db, student_id)
    if not record:
        raise HTTPException(status_code=404, detail="Academic record not found")
    return record
