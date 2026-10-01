import os
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib


INPUT_FILE = "dataset/raw/6g_network_traffic.csv"

OUTPUT_DIR = "dataset/processed"

X_TRAIN_FILE = f"{OUTPUT_DIR}/X_train.csv"
X_TEST_FILE = f"{OUTPUT_DIR}/X_test.csv"
Y_TRAIN_FILE = f"{OUTPUT_DIR}/y_train.csv"
Y_TEST_FILE = f"{OUTPUT_DIR}/y_test.csv"

SCALER_FILE = "models/scaler.joblib"
LABEL_ENCODER_FILE = "models/label_encoder.joblib"


def preprocess_dataset():

    print("=" * 70)
    print("6G CYBER DEFENSE - DATA PREPROCESSING")
    print("=" * 70)

    # --------------------------------------------------
    # 1. Load dataset
    # --------------------------------------------------

    print("\n[1/7] Loading dataset...")

    df = pd.read_csv(INPUT_FILE)

    print(f"Dataset shape: {df.shape}")

    # --------------------------------------------------
    # 2. Remove unnecessary columns
    # --------------------------------------------------

    print("\n[2/7] Removing non-ML columns...")

    columns_to_remove = [
        "flow_id",
        "timestamp",
        "source_ip",
        "destination_ip"
    ]

    existing_columns = [
        column
        for column in columns_to_remove
        if column in df.columns
    ]

    df = df.drop(
        columns=existing_columns
    )

    print(
        "Removed:",
        existing_columns
    )

    # --------------------------------------------------
    # 3. Separate features and target
    # --------------------------------------------------

    print("\n[3/7] Separating features and labels...")

    if "label" not in df.columns:
        raise ValueError(
            "Dataset does not contain 'label' column."
        )

    X = df.drop(
        columns=["label"]
    )

    y = df["label"]

    print("Features:")
    print(list(X.columns))

    print("\nLabels:")
    print(y.value_counts())

    # --------------------------------------------------
    # 4. Encode categorical features
    # --------------------------------------------------

    print("\n[4/7] Encoding categorical features...")

    categorical_columns = [
        "protocol",
        "application"
    ]

    X = pd.get_dummies(
        X,
        columns=categorical_columns,
        dtype=int
    )

    print(
        f"Number of ML features: {X.shape[1]}"
    )

    # --------------------------------------------------
    # 5. Encode target labels
    # --------------------------------------------------

    print("\n[5/7] Encoding attack labels...")

    label_encoder = LabelEncoder()

    y_encoded = label_encoder.fit_transform(y)

    print("\nLabel mapping:")

    for index, label in enumerate(
        label_encoder.classes_
    ):
        print(
            f"{index} -> {label}"
        )

    # --------------------------------------------------
    # 6. Train/test split
    # --------------------------------------------------

    print("\n[6/7] Creating train/test split...")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y_encoded,
        test_size=0.20,
        random_state=42,
        stratify=y_encoded
    )

    print(
        f"Training samples: {len(X_train)}"
    )

    print(
        f"Testing samples: {len(X_test)}"
    )

    # --------------------------------------------------
    # 7. Scaling
    # --------------------------------------------------

    print("\n[7/7] Scaling numerical features...")

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(
        X_train
    )

    X_test_scaled = scaler.transform(
        X_test
    )

    X_train_scaled = pd.DataFrame(
        X_train_scaled,
        columns=X.columns
    )

    X_test_scaled = pd.DataFrame(
        X_test_scaled,
        columns=X.columns
    )

    # --------------------------------------------------
    # Save files
    # --------------------------------------------------

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    os.makedirs(
        "models",
        exist_ok=True
    )

    X_train_scaled.to_csv(
        X_TRAIN_FILE,
        index=False
    )

    X_test_scaled.to_csv(
        X_TEST_FILE,
        index=False
    )

    pd.DataFrame({
        "label": y_train
    }).to_csv(
        Y_TRAIN_FILE,
        index=False
    )

    pd.DataFrame({
        "label": y_test
    }).to_csv(
        Y_TEST_FILE,
        index=False
    )

    joblib.dump(
        scaler,
        SCALER_FILE
    )

    joblib.dump(
        label_encoder,
        LABEL_ENCODER_FILE
    )

    print("\n" + "=" * 70)
    print("PREPROCESSING COMPLETE")
    print("=" * 70)

    print("\nGenerated files:")

    print(X_TRAIN_FILE)
    print(X_TEST_FILE)
    print(Y_TRAIN_FILE)
    print(Y_TEST_FILE)
    print(SCALER_FILE)
    print(LABEL_ENCODER_FILE)

    print("=" * 70)


if __name__ == "__main__":
    preprocess_dataset()