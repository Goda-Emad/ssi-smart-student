"""
SSI — Configuration
Loads environment variables and exposes app settings.
"""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
DATABASE_DIR = PROJECT_ROOT / "database"
DATA_DIR = DATABASE_DIR / "data"


class Settings(BaseSettings):
    # App
    APP_NAME: str = "SSI — Smart Student Integrated"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Security
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Server
    BACKEND_HOST: str = "127.0.0.1"
    BACKEND_PORT: int = 8000
    FRONTEND_ORIGIN: str = "http://localhost:5173"

    # Database
    DATABASE_URL: str = f"sqlite:///{DATABASE_DIR / 'ssi.db'}"

    # Data files
    STUDENTS_CSV: Path = DATA_DIR / "synthetic_students.csv"
    ATTENDANCE_CSV: Path = DATA_DIR / "synthetic_attendance.csv"

    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
