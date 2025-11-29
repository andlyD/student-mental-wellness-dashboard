import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
ANIM_DIR = BASE_DIR / "assets" / "animations"


def load_lottiefile(filename: str):
    file_path = ANIM_DIR / filename
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

lottie_students = load_lottiefile("Group of people communicating.json")
lottie_thinking = load_lottiefile("Thinking.json")
lottie_doctor = load_lottiefile("Doctor, Medical, Surgeon, Healthcare Animation.json")
lottie_data_analytics = load_lottiefile("Data Analytics.json")