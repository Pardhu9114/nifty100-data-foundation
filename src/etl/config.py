from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = os.getenv(
    "DB_PATH",
    str(BASE_DIR / "db" / "nifty100.db")
)

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")