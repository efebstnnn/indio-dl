# yt-dlp GUI · İndirici

[English](#english) · Türkçe

Python ile yazılmış, [yt-dlp](https://github.com/yt-dlp/yt-dlp) tabanlı masaüstü video ve ses indirici.

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Özellikler

- Video bilgisi ve kalite seçimi
- MP4 ve MP3 indirme
- İlerleme çubuğu, iptal, kuyruk
- İndirme geçmişi
- Karanlık arayüz (Inter font)

## Kurulum

```bash
git clone https://github.com/efebstnnn/yt-dlp-uygulama.git
cd yt-dlp-uygulama
pip install -r requirements.txt
```

Font eksikse: `python scripts/download_fonts.py`

**MP3** için [FFmpeg](https://ffmpeg.org/download.html) gerekir (`PATH`’te olmalı).

## Çalıştırma

```bash
python main.py
```

## Kuyruk

1. Metin kutusuna her satıra bir URL yaz veya **Ekle** ile tek link ekle.
2. **Kuyruğu indir** ile sırayla indir.
3. **Durdur** ile iptali kes.

## Yasal uyarı

Yalnızca indirme hakkınız olan veya platform kurallarına uygun içerikleri indirin.

## Lisans

[MIT](LICENSE)

---

## English

Desktop downloader using **yt-dlp** — dark UI, queue, cancel, history.

```bash
git clone https://github.com/efebstnnn/yt-dlp-uygulama.git
cd yt-dlp-uygulama
pip install -r requirements.txt
python main.py
```

FFmpeg required for MP3.
