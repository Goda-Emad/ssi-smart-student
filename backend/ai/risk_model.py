"""
SSI — Risk Model
Loads the trained risk model and exposes a clean prediction interface.
"""

import json
import joblib
import pandas as pd
from pathlib import Path

from .feature_engineer import prepare_input

MODEL_DIR = Path(__file__).parent / "models"
MODEL_PATH = MODEL_DIR / "risk_model.pkl"
METADATA_PATH = MODEL_DIR / "metadata.json"


class RiskModel:
    """Wrapper around the trained early-warning risk model."""

    def __init__(self):
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model not found: {MODEL_PATH}")
        self.model = joblib.load(MODEL_PATH)
        self.metadata = self._load_metadata()

    def _load_metadata(self) -> dict:
        if METADATA_PATH.exists():
            with open(METADATA_PATH, "r") as f:
                return json.load(f)
        return {}

    def predict(self, data: dict | pd.DataFrame) -> dict:
        """
        Predict risk for a single student or a batch.

        Args:
            data: dict (single student) or DataFrame (batch)

        Returns:
            dict with risk_label, risk_score, and risk_level
        """
        df = pd.DataFrame([data]) if isinstance(data, dict) else data.copy()
        X = prepare_input(df)

        proba = self.model.predict_proba(X)[:, 1]
        label = (proba >= 0.5).astype(int)

        return {
            "risk_label": label.tolist(),
            "risk_score": [round(float(p) * 100, 2) for p in proba],
            "risk_level": [self._level(p) for p in proba],
        }

    @staticmethod
    def _level(proba: float) -> str:
        if proba >= 0.75:
            return "High"
        if proba >= 0.5:
            return "Medium"
        return "Low"


_risk_model_instance = None


def get_risk_model() -> RiskModel:
    """Singleton accessor for the risk model."""
    global _risk_model_instance
    if _risk_model_instance is None:
        _risk_model_instance = RiskModel()
    return _risk_model_instance
