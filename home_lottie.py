import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent / "assets" / "animations" 

def load_lottiefile(filename: str):
    file_path = BASE_DIR / filename
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

lottie_students = load_lottiefile("students_jumping.json")
lottie_client   = load_lottiefile("client.json")