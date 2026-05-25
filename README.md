# Indio

[English](#english) · Türkçe

**Indio**, yt-dlp tabanlı, Python ile yazılmış sade bir masaüstü video ve ses indirici. Bağlantıyı yapıştır, formatı seç, indir.

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Özellikler

- Video bilgisi önizleme ve kalite seçimi
- MP4 ve MP3 indirme
- İlerleme çubuğu, iptal ve kuyruk desteği
- İndirme geçmişi
- Karanlık arayüz (Inter font)

## Kurulum

```bash
git clone https://github.com/efebstnnn/indio-dl.git
cd indio-dl
pip install -r requirements.txt
```

Font eksikse: `python scripts/download_fonts.py`

## FFmpeg (MP3 için)

MP3 indirmek için FFmpeg kurulu olmalı ve terminalde `ffmpeg` komutu tanınmalı.

### Windows

**Yöntem 1 — winget (önerilen)**

PowerShell'i yönetici olarak aç:

```powershell
winget install --id Gyan.FFmpeg -e
```

Kurulumdan sonra **terminali ve uygulamayı kapatıp yeniden aç**, sonra kontrol et:

```powershell
ffmpeg -version
```

Sürüm bilgisi görünüyorsa tamam.

**Yöntem 2 — elle**

1. [FFmpeg Windows builds](https://www.gyan.dev/ffmpeg/builds/) → `ffmpeg-release-essentials.zip` indir
2. Zip'i aç (ör. `C:\ffmpeg`)
3. `bin` klasörünün yolunu PATH'e ekle:
   - **Ayarlar** → "ortam değişkenleri" → **Path** → **Yeni** → `C:\ffmpeg\bin`
4. Terminali yeniden aç → `ffmpeg -version`

### macOS

```bash
brew install ffmpeg
ffmpeg -version
```

### Linux (Debian / Ubuntu)

```bash
sudo apt update
sudo apt install ffmpeg
ffmpeg -version
```

### Sorun giderme

| Belirti | Çözüm |
|--------|--------|
| `ffmpeg` tanınmıyor | PATH'e eklendi mi, terminal yeniden açıldı mı kontrol et |
| MP3 hatası uygulamada | `ffmpeg -version` çalışıyorsa uygulamayı da yeniden başlat |
| winget bulunamadı | [winget](https://learn.microsoft.com/en-us/windows/package-manager/winget/) kur veya elle indirme yöntemini kullan |

## Çalıştırma

```bash
python main.py
```

## Kuyruk

1. Metin kutusuna her satıra bir URL yaz veya **Ekle** ile tek link ekle.
2. **Kuyruğu indir** ile sırayla indir.
3. **Durdur** ile iptali kes.

## Geliştirme Süreci

Bu proje geliştirilirken yapay zeka araçlarından yararlanıldı.

## Yasal Uyarı

Yalnızca indirme hakkınız olan veya platform kurallarına uygun içerikleri indirin.

## Lisans

[MIT](LICENSE)

---

## English

**Indio** is a simple desktop video and audio downloader built with Python and yt-dlp. Paste a link, pick a format, done.

```bash
git clone https://github.com/efebstnnn/indio-dl.git
cd indio-dl
pip install -r requirements.txt
python main.py
```

**FFmpeg** is required for MP3. On Windows: `winget install --id Gyan.FFmpeg -e`, then restart the terminal and run `ffmpeg -version`. See the Turkish section above for macOS/Linux and troubleshooting.

## Development

AI tools were used during the development of this project.