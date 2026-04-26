from pathlib import Path


STUDENT_ID = "2022204011"
STUDENT_NAME = "이아란"
VALID_USERNAME = "ahran"
VALID_PASSWORD = "1234"

ASSETS_DIR = Path("assets")
PODIUM_IMAGE_PATH = ASSETS_DIR / "podium" / "podium.png"
DRIVER_IMAGE_DIR = ASSETS_DIR / "drivers"
DRIVERS_JSON_PATH = ASSETS_DIR / "drivers.json"
QUESTIONS_JSON_PATH = ASSETS_DIR / "questions.json"

PAGE_CONFIG = {
    "page_title": "나의 F1 최애 드라이버는?!",
    "page_icon": "🏁",
    "layout": "wide",
}
