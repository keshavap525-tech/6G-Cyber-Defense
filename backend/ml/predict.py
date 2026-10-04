import os
import joblib
import pandas as pd


class IntrusionDetector:

    def __init__(self):

        self.model = None
        self.scaler = None
        self.label_encoder = None

        # --------------------------------------------------
        # Project root
        # --------------------------------------------------

        BASE_DIR = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../..")
        )

        # --------------------------------------------------
        # Model paths
        # --------------------------------------------------

        model_path = os.path.join(
            BASE_DIR,
            "models",
            "intrusion_detection_model.joblib"
        )

        scaler_path = os.path.join(
            BASE_DIR,
            "models",
            "scaler.joblib"
        )

        encoder_path = os.path.join(
            BASE_DIR,
            "models",
            "label_encoder.joblib"
        )

        # --------------------------------------------------
        # Load ML model
        # --------------------------------------------------

        print(f"Looking for ML model at: {model_path}")

        try:

            self.model = joblib.load(model_path)

            print(
                f"ML model loaded from: {model_path}"
            )

        except Exception as e:

            print(
                f"Could not load ML model: {e}"
            )

        # --------------------------------------------------
        # Load scaler
        # --------------------------------------------------

        try:

            self.scaler = joblib.load(
                scaler_path
            )

            print(
                f"Scaler loaded from: {scaler_path}"
            )

        except Exception as e:

            print(
                f"Could not load scaler: {e}"
            )

        # --------------------------------------------------
        # Load label encoder
        # --------------------------------------------------

        try:

            self.label_encoder = joblib.load(
                encoder_path
            )

            print(
                f"Label encoder loaded from: {encoder_path}"
            )

        except Exception as e:

            print(
                f"Could not load label encoder: {e}"
            )

        # --------------------------------------------------
        # Expected model features
        # --------------------------------------------------

        self.feature_columns = [

            "source_port",
            "destination_port",
            "packet_size",
            "duration",
            "packets_sent",
            "packets_received",
            "bytes_sent",
            "bytes_received",
            "connection_attempts",
            "packet_number",

            "protocol_HTTP",
            "protocol_HTTPS",
            "protocol_QUIC",
            "protocol_TCP",
            "protocol_UDP",

            "application_authentication",
            "application_autonomous_vehicle",
            "application_botnet",
            "application_cloud",
            "application_data_transfer",
            "application_iot",
            "application_mobile_app",
            "application_network_scanner",
            "application_smart_city",
            "application_telemedicine",
            "application_video_streaming",
            "application_web",
        ]

        if self.model is not None:

            print(
                "Intrusion detection model loaded successfully."
            )

    # ==================================================
    # FEATURE PREPARATION
    # ==================================================

    def prepare_features(self, traffic):

        """
        Convert simulator traffic into the exact
        27-feature format used during ML training.
        """

        # --------------------------------------------------
        # Start with numerical features
        # --------------------------------------------------

        data = {

            "source_port": traffic.get(
                "src_port",
                traffic.get("source_port", 0)
            ),

            "destination_port": traffic.get(
                "dst_port",
                traffic.get("destination_port", 0)
            ),

            "packet_size": traffic.get(
                "packet_size",
                0
            ),

            "duration": traffic.get(
                "duration",
                0
            ),

            "packets_sent": traffic.get(
                "packets_sent",
                traffic.get("packet_count", 0)
            ),

            "packets_received": traffic.get(
                "packets_received",
                0
            ),

            "bytes_sent": traffic.get(
                "bytes_sent",
                traffic.get("bytes", 0)
            ),

            "bytes_received": traffic.get(
                "bytes_received",
                0
            ),

            "connection_attempts": traffic.get(
                "connection_attempts",
                0
            ),

            "packet_number": traffic.get(
                "packet_number",
                traffic.get("packet_count", 0)
            ),
        }

        # --------------------------------------------------
        # Protocol
        # --------------------------------------------------

        protocol = str(
            traffic.get(
                "protocol",
                "TCP"
            )
        ).upper()

        data["protocol_HTTP"] = int(
            protocol == "HTTP"
        )

        data["protocol_HTTPS"] = int(
            protocol == "HTTPS"
        )

        data["protocol_QUIC"] = int(
            protocol == "QUIC"
        )

        data["protocol_TCP"] = int(
            protocol == "TCP"
        )

        data["protocol_UDP"] = int(
            protocol == "UDP"
        )

        # --------------------------------------------------
        # Application
        # --------------------------------------------------

        application = str(
            traffic.get(
                "application",
                "iot"
            )
        ).lower()

        application_columns = [

            "authentication",
            "autonomous_vehicle",
            "botnet",
            "cloud",
            "data_transfer",
            "iot",
            "mobile_app",
            "network_scanner",
            "smart_city",
            "telemedicine",
            "video_streaming",
            "web",
        ]

        for app in application_columns:

            column = f"application_{app}"

            data[column] = int(
                application == app
            )

        # --------------------------------------------------
        # DataFrame
        # --------------------------------------------------

        df = pd.DataFrame(
            [data]
        )

        # --------------------------------------------------
        # Ensure exact feature order
        # --------------------------------------------------

        df = df[
            self.feature_columns
        ]

        # --------------------------------------------------
        # Numeric conversion
        # --------------------------------------------------

        df = df.apply(
            pd.to_numeric,
            errors="coerce"
        )

        df = df.fillna(0)

        return df

    # ==================================================
    # PREDICTION
    # ==================================================

    def predict(self, traffic):

        """
        Run the trained Random Forest model.
        """

        features = self.prepare_features(
            traffic
        )

        # --------------------------------------------------
        # Make sure ML components exist
        # --------------------------------------------------

        if (
            self.model is None
            or self.scaler is None
        ):

            print(
                "ML components unavailable."
            )

            return self.demo_prediction(
                traffic
            )

        try:

            # --------------------------------------------------
            # Scale exactly like training
            # --------------------------------------------------

            scaled_features = (
                self.scaler.transform(
                    features
                )
            )

            scaled_df = pd.DataFrame(
                scaled_features,
                columns=self.feature_columns
            )

            # --------------------------------------------------
            # Prediction
            # --------------------------------------------------

            prediction = self.model.predict(
                scaled_df
            )[0]

            # --------------------------------------------------
            # Decode label
            # --------------------------------------------------

            if self.label_encoder is not None:

                try:

                    prediction_label = (
                        self.label_encoder.inverse_transform(
                            [prediction]
                        )[0]
                    )

                except Exception:

                    prediction_label = str(
                        prediction
                    )

            else:

                prediction_label = str(
                    prediction
                )

            # --------------------------------------------------
            # Probability
            # --------------------------------------------------

            threat_score = 0.0

            if hasattr(
                self.model,
                "predict_proba"
            ):

                probabilities = (
                    self.model.predict_proba(
                        scaled_df
                    )[0]
                )

                threat_score = float(
                    max(probabilities)
                )

            print(
                f"[ML] Prediction={prediction_label} "
                f"| confidence={threat_score:.3f}"
            )

            return {

                "prediction": str(
                    prediction_label
                ),

                "threat_score": round(
                    threat_score,
                    3
                ),
            }

        except Exception as e:

            print(
                f"Model prediction error: {e}"
            )

            return self.demo_prediction(
                traffic
            )

    # ==================================================
    # DEMO FALLBACK
    # ==================================================

    def demo_prediction(self, traffic):

        packet_count = float(
            traffic.get(
                "packet_count",
                0
            )
        )

        packet_size = float(
            traffic.get(
                "packet_size",
                0
            )
        )

        duration = float(
            traffic.get(
                "duration",
                0
            )
        )

        bytes_sent = float(
            traffic.get(
                "bytes_sent",
                traffic.get("bytes", 0)
            )
        )

        bytes_received = float(
            traffic.get(
                "bytes_received",
                0
            )
        )

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

        score = min(
            score,
            1.0
        )

        if score >= 0.5:

            prediction = "ATTACK"

        else:

            prediction = "NORMAL"

        return {

            "prediction": prediction,

            "threat_score": round(
                score,
                3
            ),
        }
