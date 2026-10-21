"""
SSI — Early Warning Router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas.risk import RiskResponse, AtRiskStudent
from services.risk_service import predict_student_risk, get_at_risk_students

router = APIRouter()


@router.get("/at-risk", response_model=list[AtRiskStudent])
def at_risk(db: Session = Depends(get_db)):
    return get_at_risk_students(db)


@router.get("/{student_id}", response_model=RiskResponse)
def predict(student_id: str, db: Session = Depends(get_db)):
    result = predict_student_risk(db, student_id)
    if not result:
        raise HTTPException(status_code=404, detail="Student not found")
    return result
