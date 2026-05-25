# yt-dlp GUI · İndirici

[English](#english) · Türkçe

Python ile yazılmış, [yt-dlp](https://github.com/yt-dlp/yt-dlp) tabanlı masaüstü video ve ses indirici. Windows, macOS ve Linux’ta çalışır.

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Repo](https://img.shields.io/badge/GitHub-efebstnnn%2Fyt--dlp--uygulama-24292f?logo=github)](https://github.com/efebstnnn/yt-dlp-uygulama)

## Önizleme

> Ekran görüntüsü: uygulamayı aç → `Win + Shift + S` → `docs/screenshots/app.png` kaydet → aşağıdaki satırın yorumunu kaldır:
>
> `![Arayüz](docs/screenshots/app.png)`

## Özellikler

- Bağlantıdan video bilgisi ve kalite listesi
- **MP4** (video) ve **MP3** (ses) indirme
- İlerleme: yüzde, hız, kalan süre
- İndirmeyi **durdurma**
- **Kuyruk** — tek link veya çok satırlı toplu ekleme
- İndirme geçmişi ve geçmişten tekrar yükleme
- Son klasörü hatırlama
- MP3 için FFmpeg kontrolü
- Karanlık arayüz, **Inter** font

## Gereksinimler

| Yazılım | Zorunlu | Not |
|---------|---------|-----|
| Python 3.10+ | Evet | [python.org](https://www.python.org/downloads/) |
| yt-dlp | Evet | `requirements.txt` ile kurulur |
| FFmpeg | MP3 için | [ffmpeg.org](https://ffmpeg.org/download.html) — `PATH`’te olmalı |

## Kurulum

```bash
git clone https://github.com/efebstnnn/yt-dlp-uygulama.git
cd yt-dlp-uygulama
pip install -r requirements.txt
```

Fontlar repoda gelir (`assets/fonts/`). Eksikse:

```bash
python scripts/download_fonts.py
```

## Çalıştırma

```bash
python main.py
```

## Kuyruk

1. Üstteki kutuya her satıra bir URL yaz veya **Metinden al** kullan.
2. Format ve kaliteyi seç; **Ekle** ile tek link de eklenebilir.
3. **Kuyruğu indir** ile sırayla indirilir.
4. **Durdur** ile aktif indirmeyi keser.

## Proje yapısı

```
yt-dlp-uygulama/
├── main.py              # Giriş noktası
├── gui.py               # Arayüz
├── downloader.py        # yt-dlp mantığı
├── theme.py / fonts.py  # Görünüm
├── version.py           # Sürüm numarası
├── assets/fonts/        # Inter (.ttf)
├── scripts/             # Yardımcı scriptler
├── docs/                # Dokümantasyon
└── requirements.txt
```

## Yasal uyarı

Yalnızca indirme hakkınız olan veya platform kurallarına uygun içerikleri indirin. Telif ve hizmet şartlarına uygunluk **kullanıcının sorumluluğundadır**. Bu araç eğitim ve kişisel kullanım içindir; yt-dlp’nin desteklediği sitelerin kurallarına tabidir.

## Katkı

Hata ve öneriler için [Issue aç](https://github.com/efebstnnn/yt-dlp-uygulama/issues). Yol haritası: [ROADMAP.md](ROADMAP.md).

## Lisans

[MIT](LICENSE) — Copyright (c) 2026 [efebstnnn](https://github.com/efebstnnn)

---

## English

Desktop app to download video/audio via **yt-dlp**, with a dark UI (CustomTkinter), download queue, cancel, and history.

```bash
git clone https://github.com/efebstnnn/yt-dlp-uygulama.git
cd yt-dlp-uygulama
pip install -r requirements.txt
python main.py
```

**FFmpeg** required for MP3. Repo: [github.com/efebstnnn/yt-dlp-uygulama](https://github.com/efebstnnn/yt-dlp-uygulama)
