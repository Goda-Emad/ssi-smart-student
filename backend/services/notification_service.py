"""
SSI — Notification Service
"""

from utils.logger import get_logger

logger = get_logger(__name__)


def send_risk_notification(student_id: str, risk_level: str, message: str = None):
    """
    Placeholder notification sender.
    In production: integrate email / SMS / in-app notifications.
    """
    if message is None:
        message = f"Student {student_id} has been flagged as {risk_level} risk."

    logger.info(f"[NOTIFICATION] {message}")
    return {"student_id": student_id, "risk_level": risk_level, "sent": True}
