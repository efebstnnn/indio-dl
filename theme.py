"""Uygulama genelinde renk, tipografi ve bileşen stilleri."""

from typing import Optional

import fonts


def _font(size: int, weight: Optional[str] = None) -> tuple:
    aile = fonts.aile()
    if weight:
        return (aile, size, weight)
    return (aile, size)


class Tema:
    # Arka plan ve yüzeyler
    BG = "#111113"
    SURFACE = "#1a1a1d"
    SURFACE_ELEVATED = "#232326"
    BORDER = "#2e2e32"

    # Metin
    TEXT = "#ececea"
    TEXT_SECONDARY = "#a8a8ad"
    TEXT_DIM = "#6b6b70"

    # Tek vurgu rengi (sıcak, sakin)
    ACCENT = "#d4a574"
    ACCENT_HOVER = "#c49563"
    ACCENT_MUTED = "#3d3529"

    # Durumlar — pastel, bağırmayan
    OK = "#7d9b8a"
    WARN = "#b8a066"
    ERR = "#b87a7a"

    # Bileşenler
    INPUT = "#1e1e21"
    INPUT_BORDER = "#333338"
    BTN_SECONDARY = "#2a2a2e"
    BTN_SECONDARY_HOVER = "#35353a"
    BTN_GHOST_HOVER = "#2a2a2e"

    RADIUS = 12
    RADIUS_SM = 8

    @staticmethod
    def guncelle_fontlar():
        """Fontlar yüklendikten sonra çağrılır."""
        Tema.FONT = _font(13)
        Tema.FONT_SM = _font(11)
        Tema.FONT_XS = _font(10)
        Tema.FONT_TITLE = _font(20, "bold")
        Tema.FONT_SECTION = _font(10)
        Tema.FONT_BTN = _font(13)
        Tema.FONT_BTN_PRIMARY = _font(14, "bold")

    # Varsayılan (yükleme öncesi yedek)
    FONT = _font(13)
    FONT_SM = _font(11)
    FONT_XS = _font(10)
    FONT_TITLE = _font(20, "bold")
    FONT_SECTION = _font(10)
    FONT_BTN = _font(13)
    FONT_BTN_PRIMARY = _font(14, "bold")


def bolum_etiketi(parent, metin: str, **kwargs) -> "ctk.CTkLabel":
    import customtkinter as ctk

    return ctk.CTkLabel(
        parent,
        text=metin,
        font=Tema.FONT_SECTION,
        text_color=Tema.TEXT_DIM,
        anchor="w",
        **kwargs,
    )
