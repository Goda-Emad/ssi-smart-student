"""
SSI — Students Router
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import io
import qrcode

from database import get_db
from schemas.student import StudentResponse
from services.student_service import get_student_by_student_id

router = APIRouter()


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: str, db: Session = Depends(get_db)):
    student = get_student_by_student_id(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.get("/{student_id}/qr")
def get_student_qr(student_id: str, db: Session = Depends(get_db)):
    student = get_student_by_student_id(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(student.student_id)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#173142", back_color="white")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")
