import base64
import json
from pathlib import Path

import streamlit as st

from src.config import DRIVER_IMAGE_DIR, DRIVERS_JSON_PATH, QUESTIONS_JSON_PATH


@st.cache_data
def load_drivers():
    # Driver data is static for the assignment, so caching avoids re-reading
    # the JSON file on every Streamlit rerun.
    return json.loads(DRIVERS_JSON_PATH.read_text(encoding="utf-8-sig"))


@st.cache_data
def load_questions():
    # The quiz definitions are static data, so caching prevents re-reading
    # the JSON file every time a widget triggers a rerun.
    return json.loads(QUESTIONS_JSON_PATH.read_text(encoding="utf-8-sig"))


def get_driver_map(drivers):
    return {driver["id"]: driver for driver in drivers}


def get_driver_profile_image_path(driver: dict) -> Path:
    image_id_overrides = {
        "alexander_albon": "alex_albon",
    }
    image_key = image_id_overrides.get(driver["id"], driver["id"])

    for extension in (".jpg", ".png", ".jpeg"):
        image_path = DRIVER_IMAGE_DIR / f"{image_key}{extension}"
        if image_path.exists():
            return image_path
    return None


def encode_image_to_base64(image_path) -> str:
    if not image_path:
        return ""

    path = Path(image_path)
    if not path.exists():
        return ""

    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()
