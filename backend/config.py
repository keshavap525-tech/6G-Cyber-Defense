import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_NAME = "AI-Powered 6G Cyber Defense System"

HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./cyber_defense.db"
)

MODEL_PATH = os.getenv(
    "MODEL_PATH",
    "models/intrusion_detection_model.joblib"
)