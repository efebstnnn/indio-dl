import json
import os

CONFIG_PATH = "config.json"


def yukle() -> dict:
    if not os.path.exists(CONFIG_PATH):
        return {}
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def kaydet(indirme_klasoru: str) -> None:
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump({"indirme_klasoru": indirme_klasoru}, f, ensure_ascii=False, indent=2)
    except OSError as e:
        print(f"Ayarlar kaydedilemedi: {e}")
