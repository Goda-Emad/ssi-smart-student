"""
SSI — Feature Engineering
Transforms raw student data into features expected by the risk model.
"""

import pandas as pd

# Columns that are NOT model features
DROP_COLS = ["student_id", "full_name", "risk_label"]


def split_features_target(df: pd.DataFrame, target: str = "risk_label"):
    """
    Split a dataframe into features (X) and target (y).
    """
    df = df.copy()
    X = df.drop(columns=[c for c in DROP_COLS if c in df.columns])
    y = df[target] if target in df.columns else None
    return X, y


def get_column_types(df: pd.DataFrame):
    """
    Return numeric and categorical column names.
    """
    num_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    cat_cols = df.select_dtypes(include=["object"]).columns.tolist()
    return num_cols, cat_cols


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add derived features used to improve risk prediction.
    """
    df = df.copy()

    if {"credits_completed", "total_credits"}.issubset(df.columns):
        df["completion_ratio"] = (
            df["credits_completed"] / df["total_credits"].replace(0, pd.NA)
        ).fillna(0.0)

    if {"absence_days", "attendance_rate"}.issubset(df.columns):
        df["absence_rate"] = 100.0 - df["attendance_rate"]

    if {"failed_courses_count", "current_semester"}.issubset(df.columns):
        df["fail_rate"] = (
            df["failed_courses_count"] / df["current_semester"].replace(0, pd.NA)
        ).fillna(0.0)

    if {"lms_logins", "library_visits"}.issubset(df.columns):
        df["engagement_score"] = df["lms_logins"] + df["library_visits"]

    return df


def prepare_input(df: pd.DataFrame) -> pd.DataFrame:
    """
    Full pipeline: engineer features and drop non-feature columns.
    """
    df = engineer_features(df)
    X, _ = split_features_target(df)
    return X
