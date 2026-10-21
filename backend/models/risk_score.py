"""
SSI — RiskScore Model
"""

from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class RiskScore(Base):
    __tablename__ = "risk_scores"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(
        Integer,
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    risk_label = Column(Integer, nullable=False)          # 0 = safe, 1 = at risk
    risk_score = Column(Float, nullable=False)            # 0–100
    risk_level = Column(String(20), nullable=False)       # Low / Medium / High
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("Student", back_populates="risk_scores")
