import os
import time

import joblib
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import (
    RandomForestClassifier,
    ExtraTreesClassifier,
    GradientBoostingClassifier
)

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)


X_TRAIN_FILE = "dataset/processed/X_train.csv"
X_TEST_FILE = "dataset/processed/X_test.csv"

Y_TRAIN_FILE = "dataset/processed/y_train.csv"
Y_TEST_FILE = "dataset/processed/y_test.csv"

MODEL_DIR = "models"


def load_data():

    X_train = pd.read_csv(
        X_TRAIN_FILE
    )

    X_test = pd.read_csv(
        X_TEST_FILE
    )

    y_train = pd.read_csv(
        Y_TRAIN_FILE
    )["label"]

    y_test = pd.read_csv(
        Y_TEST_FILE
    )["label"]

    return (
        X_train,
        X_test,
        y_train,
        y_test
    )


def evaluate_model(
    model,
    X_test,
    y_test
):

    predictions = model.predict(
        X_test
    )

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    precision = precision_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    return (
        accuracy,
        precision,
        recall,
        f1,
        predictions
    )


def main():

    print("=" * 80)
    print("AI 6G CYBER DEFENSE - ML MODEL TRAINING")
    print("=" * 80)

    # --------------------------------------------------
    # Load data
    # --------------------------------------------------

    print("\nLoading processed dataset...")

    (
        X_train,
        X_test,
        y_train,
        y_test
    ) = load_data()

    print(
        f"Training samples: {len(X_train)}"
    )

    print(
        f"Testing samples: {len(X_test)}"
    )

    print(
        f"Features: {X_train.shape[1]}"
    )

    # --------------------------------------------------
    # Define models
    # --------------------------------------------------

    models = {

        "Logistic Regression":
            LogisticRegression(
                max_iter=1000,
                random_state=42
            ),

        "Random Forest":
            RandomForestClassifier(
                n_estimators=200,
                random_state=42,
                n_jobs=-1
            ),

        "Extra Trees":
            ExtraTreesClassifier(
                n_estimators=200,
                random_state=42,
                n_jobs=-1
            ),

        "Gradient Boosting":
            GradientBoostingClassifier(
                random_state=42
            )
    }

    results = []

    trained_models = {}

    # --------------------------------------------------
    # Train models
    # --------------------------------------------------

    for name, model in models.items():

        print("\n" + "-" * 80)

        print(
            f"Training: {name}"
        )

        start_time = time.time()

        model.fit(
            X_train,
            y_train
        )

        training_time = (
            time.time() - start_time
        )

        (
            accuracy,
            precision,
            recall,
            f1,
            predictions
        ) = evaluate_model(
            model,
            X_test,
            y_test
        )

        trained_models[name] = model

        results.append({
            "model": name,
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
            "training_time_seconds":
                training_time
        })

        print(
            f"Accuracy : {accuracy:.4f}"
        )

        print(
            f"Precision: {precision:.4f}"
        )

        print(
            f"Recall   : {recall:.4f}"
        )

        print(
            f"F1 Score : {f1:.4f}"
        )

        print(
            f"Training : {training_time:.2f}s"
        )

        print("\nClassification Report:")

        print(
            classification_report(
                y_test,
                predictions,
                zero_division=0
            )
        )

    # --------------------------------------------------
    # Results
    # --------------------------------------------------

    results_df = pd.DataFrame(
        results
    )

    results_df = results_df.sort_values(
        by="f1_score",
        ascending=False
    )

    print("\n")
    print("=" * 80)
    print("MODEL COMPARISON")
    print("=" * 80)

    print(
        results_df.to_string(
            index=False
        )
    )

    # --------------------------------------------------
    # Select model using F1 score
    # --------------------------------------------------

    best_model_name = results_df.iloc[0]["model"]

    best_model = trained_models[
        best_model_name
    ]

    print("\n")
    print(
        f"Selected model based on weighted F1: "
        f"{best_model_name}"
    )

    # --------------------------------------------------
    # Save model
    # --------------------------------------------------

    os.makedirs(
        MODEL_DIR,
        exist_ok=True
    )

    production_model_path = (
        f"{MODEL_DIR}/intrusion_detection_model.joblib"
    )

    joblib.dump(
        best_model,
        production_model_path
    )

    # Save comparison
    results_df.to_csv(
        f"{MODEL_DIR}/model_comparison.csv",
        index=False
    )

    print("\nSaved:")

    print(
        production_model_path
    )

    print(
        f"{MODEL_DIR}/model_comparison.csv"
    )

    print("\n")
    print("=" * 80)
    print("MODEL TRAINING COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()