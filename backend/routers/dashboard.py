"""
SSI — Dashboard Router
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from services.dashboard_service import get_summary

router = APIRouter()


@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    return get_summary(db)
