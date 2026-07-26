"""Central paths & flags for the project."""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR     = PROJECT_ROOT / "data"
UPLOADS_DIR  = DATA_DIR / "uploads"
OUTPUTS_DIR  = DATA_DIR / "outputs"

UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

USE_DOCKER = os.getenv("USE_DOCKER", "false").lower() == "true"
