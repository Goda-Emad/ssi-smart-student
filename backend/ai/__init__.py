"""
SSI AI module.

Provides the trained early-warning risk model and helpers
for loading and running inference.
"""

from pathlib import Path

MODEL_DIR = Path(__file__).parent / "models"
MODEL_PATH = MODEL_DIR / "risk_model.pkl"
METADATA_PATH = MODEL_DIR / "metadata.json"

__all__ = ["MODEL_DIR", "MODEL_PATH", "METADATA_PATH"]
