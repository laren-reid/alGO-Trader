import os
import sys

import joblib
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import FEATURE_COLUMNS, MODEL_PATH
from features import add_features, chronological_split
from model import create_model


def train(df, verbose: bool = True):
    """
    Trains the model on the first 80% of the data (chronological split -
    no shuffling, since shuffling time series data leaks future info into
    training) and evaluates on the held-out last 20%.

    Returns (model, metrics). Metrics previously went uncomputed entirely -
    a model that "trains successfully" tells you nothing about whether
    it's actually useful.
    """

    df = add_features(df)

    train_df, test_df = chronological_split(df, train_frac=0.8)

    X_train = train_df[FEATURE_COLUMNS]
    y_train = train_df["Target"]

    X_test = test_df[FEATURE_COLUMNS]
    y_test = test_df["Target"]

    model = create_model()
    model.fit(X_train, y_train)

    metrics = None
    if len(X_test) > 0:
        y_pred = model.predict(X_test)
        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred, zero_division=0),
            "recall": recall_score(y_test, y_pred, zero_division=0),
            "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
            "test_samples": len(X_test),
            "majority_class_baseline": max(y_test.mean(), 1 - y_test.mean()),
        }

        if verbose:
            print(f"[Train] Test samples: {metrics['test_samples']}")
            print(f"[Train] Accuracy:  {metrics['accuracy']:.3f}  (majority-class baseline: {metrics['majority_class_baseline']:.3f})")
            print(f"[Train] Precision: {metrics['precision']:.3f}")
            print(f"[Train] Recall:    {metrics['recall']:.3f}")
            print(f"[Train] Confusion matrix [[TN, FP], [FN, TP]]: {metrics['confusion_matrix']}")
    elif verbose:
        print("[Train] Warning: no test samples available (dataset too small for an 80/20 split); skipping evaluation.")

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    if verbose:
        print(f"[Train] Model saved to {MODEL_PATH}")

    return model, metrics
