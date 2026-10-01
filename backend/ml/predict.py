import os
import joblib
import pandas as pd
import numpy as np


class IntrusionDetector:

    def __init__(self):
        self.model = None
        self.feature_columns = []

        # Try to find a trained model
        model_paths = [
            "backend/ml/model.pkl",
            "backend/ml/intrusion_model.pkl",
            "models/model.pkl",
            "model.pkl",
        ]

        for path in model_paths:
            if os.path.exists(path):
                try:
                    self.model = joblib.load(path)
                    print(f"ML model loaded from: {path}")
                    break
                except Exception as e:
                    print(f"Could not load model {path}: {e}")

        if self.model is None:
            print("No trained ML model found.")
            print("Running in demo mode.")

        print("Intrusion detection model loaded.")

    def prepare_features(self, traffic):
        """
        Convert incoming traffic data into a DataFrame.
        """

        # Convert dictionary to DataFrame
        df = pd.DataFrame([traffic])

        # Expected basic traffic fields
        expected_columns = [
            "packet_count",
            "packet_size",
            "duration",
            "bytes_sent",
            "bytes_received",
        ]

        # Add missing numeric columns
        for column in expected_columns:
            if column not in df.columns:
                df[column] = 0

        # Keep only known numeric features for now
        df = df[expected_columns]

        # Convert values to numeric
        df = df.apply(pd.to_numeric, errors="coerce")

        # Replace invalid values
        df = df.fillna(0)

        return df

    def predict(self, traffic):
        """
        Predict whether the traffic is normal or suspicious.
        """

        features = self.prepare_features(traffic)

        # If a trained model exists, use it
        if self.model is not None:

            try:
                prediction = self.model.predict(features)[0]

                # Try to obtain probability
                threat_score = 0.0

                if hasattr(self.model, "predict_proba"):
                    probabilities = self.model.predict_proba(features)[0]
                    threat_score = float(max(probabilities))

                return {
                    "prediction": str(prediction),
                    "threat_score": threat_score,
                }

            except Exception as e:

                print(f"Model prediction error: {e}")

        # Demo fallback
        packet_count = float(
            traffic.get("packet_count", 0)
        )

        packet_size = float(
            traffic.get("packet_size", 0)
        )

        duration = float(
            traffic.get("duration", 0)
        )

        bytes_sent = float(
            traffic.get("bytes_sent", 0)
        )

        bytes_received = float(
            traffic.get("bytes_received", 0)
        )

        # Simple demonstration detection logic
        score = 0.0

        if packet_count > 1000:
            score += 0.25

        if packet_size > 1500:
            score += 0.20

        if duration < 1 and packet_count > 100:
            score += 0.20

        if bytes_sent > 1000000:
            score += 0.15

        if bytes_received > 1000000:
            score += 0.15

        score = min(score, 1.0)

        if score >= 0.5:
            prediction = "ATTACK"
        else:
            prediction = "NORMAL"

        return {
            "prediction": prediction,
            "threat_score": round(score, 3),
        }