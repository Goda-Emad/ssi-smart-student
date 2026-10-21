"""
SSI — Smart ID Service
"""

import io
import qrcode

from models.student import Student


def generate_qr_for_student(student: Student) -> io.BytesIO:
    """
    Generate a QR code PNG (in-memory) for a student's Smart ID.
    """
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(student.student_id)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#173142", back_color="white")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf
