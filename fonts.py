"""Inter font dosyalarını CustomTkinter'a yükler."""

from pathlib import Path

import customtkinter as ctk

FONT_DIR = Path(__file__).resolve().parent / "assets" / "fonts"
FAMILY = "Inter"

FONT_DOSYALARI = (
    "Inter-Regular.ttf",
    "Inter-Medium.ttf",
    "Inter-SemiBold.ttf",
)

_yuklendi = False


def yukle() -> bool:
    """Fontları bir kez yükler. Başarılıysa True döner."""
    global _yuklendi
    if _yuklendi:
        return True

    bulunan = 0
    for dosya in FONT_DOSYALARI:
        yol = FONT_DIR / dosya
        if yol.is_file():
            ctk.FontManager.load_font(str(yol))
            bulunan += 1

    _yuklendi = bulunan > 0
    return _yuklendi


def aile() -> str:
    """Arayüzde kullanılacak font ailesi (yüklenemezse yedek)."""
    return FAMILY if _yuklendi else "Segoe UI"
