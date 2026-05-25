"""Inter font dosyalarını assets/fonts klasörüne indirir."""

import urllib.request
from pathlib import Path

FONT_DIR = Path(__file__).resolve().parent.parent / "assets" / "fonts"

URLS = {
    "Inter-Regular.ttf": "https://cdn.jsdelivr.net/fontsource/fonts/inter@5.0.16/latin-400-normal.ttf",
    "Inter-Medium.ttf": "https://cdn.jsdelivr.net/fontsource/fonts/inter@5.0.16/latin-500-normal.ttf",
    "Inter-SemiBold.ttf": "https://cdn.jsdelivr.net/fontsource/fonts/inter@5.0.16/latin-600-normal.ttf",
}


def main():
    FONT_DIR.mkdir(parents=True, exist_ok=True)
    for name, url in URLS.items():
        dest = FONT_DIR / name
        print(f"İndiriliyor: {name}")
        urllib.request.urlretrieve(url, dest)
        print(f"  → {dest} ({dest.stat().st_size} byte)")


if __name__ == "__main__":
    main()
