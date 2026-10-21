"""
SSI — Training Script
Trains the early-warning risk model from synthetic_students.csv
and saves the model + metadata.
"""

import json
import joblib
import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, classification_report
)

DATA_PATH = Path(__file__).parent.parent.parent / "data" / "synthetic_students.csv"
MODEL_DIR = Path(__file__).parent / "models"
MODEL_PATH = MODEL_DIR / "risk_model.pkl"
METADATA_PATH = MODEL_DIR / "metadata.json"

TARGET = "risk_label"
DROP_COLS = ["student_id", "full_name"]
RANDOM_STATE = 42


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Data not found: {path}")
    return pd.read_csv(path)


def build_pipeline(num_cols, cat_cols) -> Pipeline:
    preprocessor = ColumnTransformer([
        ("num", StandardScaler(), num_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
    ])
    return Pipeline([
        ("prep", preprocessor),
        ("clf", RandomForestClassifier(
            n_estimators=300,
            max_depth=12,
            class_weight="balanced",
            random_state=RANDOM_STATE,
            n_jobs=-1,
        )),
    ])


def train():
    df = load_data()
    df = df.drop(columns=[c for c in DROP_COLS if c in df.columns])

    X = df.drop(columns=[TARGET])
    y = df[TARGET]

    num_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
    cat_cols = X.select_dtypes(include=["object"]).columns.tolist()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )

    model = build_pipeline(num_cols, cat_cols)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": round(accuracy_score(y_test, y_pred), 4),
        "precision": round(precision_score(y_test, y_pred), 4),
        "recall": round(recall_score(y_test, y_pred), 4),
        "f1": round(f1_score(y_test, y_pred), 4),
        "roc_auc": round(roc_auc_score(y_test, y_proba), 4),
    }
    print("Metrics:", metrics)
    print(classification_report(y_test, y_pred))

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    ohe = model.named_steps["prep"].named_transformers_["cat"]
    cat_names = ohe.get_feature_names_out(cat_cols).tolist()
    all_features = num_cols + cat_names

    importances = model.named_steps["clf"].feature_importances_
    feat_imp = (
        pd.DataFrame({"feature": all_features, "importance": importances})
        .sort_values("importance", ascending=False)
        .head(15)
        .to_dict(orient="records")
    )

    metadata = {
        "model_name": "RandomForestClassifier",
        "version": "1.0.0",
        "trained_on": DATA_PATH.name,
        "n_samples": int(len(df)),
        "target": TARGET,
        "features": list(X.columns),
        "numeric_features": num_cols,
        "categorical_features": cat_cols,
        "metrics": metrics,
        "top_features": feat_imp,
        "random_state": RANDOM_STATE,
    }
    with open(METADATA_PATH, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"Saved model  -> {MODEL_PATH}")
    print(f"Saved metadata -> {METADATA_PATH}")
    return model, metadata


if __name__ == "__main__":
    train()
