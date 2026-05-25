import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime

import yt_dlp
from yt_dlp.utils import DownloadCancelled

HISTORY_FILE = "indirme_gecmisi.json"
MAX_HISTORY = 100


class DownloadError(Exception):
    """Kullanıcıya gösterilebilir indirme hatası."""


class DownloadCancelledError(DownloadError):
    """Kullanıcı indirmeyi iptal etti."""


def ffmpeg_kurulu_mu() -> bool:
    return shutil.which("ffmpeg") is not None


def url_temizle(url: str) -> str:
    return url.strip()


class VideoDownloader:
    def __init__(self, progress_callback):
        self.progress_callback = progress_callback
        self.secilen_klasor = ""
        self._iptal = False
        self._ydl = None

    def klasor_set(self, dizin: str) -> None:
        self.secilen_klasor = dizin

    def get_hedef_dizin(self) -> str:
        return self.secilen_klasor if self.secilen_klasor else os.getcwd()

    def iptal_sifirla(self) -> None:
        self._iptal = False

    def iptal_talep_et(self) -> None:
        self._iptal = True
        if self._ydl is not None:
            try:
                self._ydl.cancel_download()
            except Exception:
                pass

    def iptal_edildi_mi(self) -> bool:
        return self._iptal

    def klasoru_ac(self) -> None:
        hedef_dizin = self.get_hedef_dizin()
        try:
            if os.name == "nt":
                os.startfile(hedef_dizin)
            elif sys.platform == "darwin":
                subprocess.run(["open", hedef_dizin], check=False)
            else:
                subprocess.run(["xdg-open", hedef_dizin], check=False)
        except OSError as e:
            print(f"Klasör açılamadı: {e}")

    def gecmisi_yukle(self) -> list:
        if not os.path.exists(HISTORY_FILE):
            return []
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                veri = json.load(f)
                return veri if isinstance(veri, list) else []
        except (json.JSONDecodeError, OSError):
            return []

    def gecmise_ekle(self, baslik: str, kalite: str, format_tipi: str, url: str) -> None:
        gecmis = self.gecmisi_yukle()
        yeni_kayit = {
            "baslik": baslik or "Bilinmeyen Video",
            "kalite": kalite,
            "format": format_tipi,
            "url": url,
            "tarih": datetime.now().strftime("%d.%m.%Y %H:%M"),
        }
        gecmis.insert(0, yeni_kayit)
        gecmis = gecmis[:MAX_HISTORY]

        try:
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(gecmis, f, ensure_ascii=False, indent=2)
        except OSError as e:
            print(f"Geçmiş kaydedilemedi: {e}")

    def bilgi_ve_kalite_cek(self, url: str) -> dict:
        url = url_temizle(url)
        if not url:
            return {"baslik": None, "kaliteler": [], "hata": "Link boş."}

        try:
            with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True}) as ydl:
                info = ydl.extract_info(url, download=False)
                baslik = info.get("title", "Bilinmeyen Video")
                formatlar = info.get("formats", [])

                kaliteler = set()
                for fmt in formatlar:
                    if fmt.get("height") and fmt.get("vcodec") != "none":
                        kaliteler.add(fmt["height"])

                sirali = [f"{h}p" for h in sorted(kaliteler, reverse=True)]
                return {"baslik": baslik, "kaliteler": sirali, "hata": None}
        except Exception as e:
            return {"baslik": None, "kaliteler": [], "hata": str(e)}

    def _ilerleme_kancasi(self, d: dict) -> None:
        if self._iptal and self._ydl is not None:
            try:
                self._ydl.cancel_download()
            except Exception:
                pass
            return

        if d.get("status") != "downloading":
            return

        yuzde_metni = d.get("_percent_str", "0.0%")
        hiz_metni = d.get("_speed_str", "0B/s").strip()
        kalan_sure = d.get("_eta_str", "00:00").strip()

        ansi_temizleyici = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]")
        temiz_hiz = ansi_temizleyici.sub("", hiz_metni)
        temiz_sure = ansi_temizleyici.sub("", kalan_sure)

        eslesme = re.search(r"(\d+\.?\d*)%", yuzde_metni)
        if eslesme:
            self.progress_callback(eslesme.group(1), temiz_hiz, temiz_sure)

    def _video_format_sec(self, kalite_secim: str) -> str:
        cozunurluk = kalite_secim.replace("p", "").strip()
        if cozunurluk.isdigit():
            h = cozunurluk
            return (
                f"bestvideo[height<={h}]+bestaudio/"
                f"best[height<={h}]/best[height<={h}]"
            )
        return "bestvideo+bestaudio/best"

    def _ydl_secenekleri(self, format_secim: str, kalite_secim: str) -> dict:
        hedef = self.get_hedef_dizin()
        ydl_opts = {
            "progress_hooks": [self._ilerleme_kancasi],
            "quiet": True,
            "no_warnings": True,
        }

        if format_secim == "MP3 (Ses)":
            ydl_opts.update(
                {
                    "format": "bestaudio/best",
                    "outtmpl": os.path.join(hedef, "%(title)s.%(ext)s"),
                    "postprocessors": [
                        {
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": "mp3",
                            "preferredquality": "192",
                        }
                    ],
                }
            )
        else:
            ydl_opts.update(
                {
                    "format": self._video_format_sec(kalite_secim),
                    "merge_output_format": "mp4",
                    "outtmpl": os.path.join(hedef, "%(title)s [%(height)sp].%(ext)s"),
                }
            )
        return ydl_opts

    def indir(self, url: str, format_secim: str, kalite_secim: str) -> str:
        url = url_temizle(url)
        if not url:
            raise DownloadError("Lütfen geçerli bir video linki girin.")

        if format_secim == "MP3 (Ses)" and not ffmpeg_kurulu_mu():
            raise DownloadError(
                "MP3 için FFmpeg gerekli. FFmpeg kurulu değil veya PATH'te bulunamadı."
            )

        ydl_opts = self._ydl_secenekleri(format_secim, kalite_secim)

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self._ydl = ydl
                try:
                    info = ydl.extract_info(url, download=True)
                finally:
                    self._ydl = None

            if self._iptal:
                raise DownloadCancelledError("İndirme iptal edildi.")

            return info.get("title", "Bilinmeyen Video")
        except DownloadCancelledError:
            raise
        except DownloadCancelled:
            raise DownloadCancelledError("İndirme iptal edildi.") from None
        except DownloadError:
            raise
        except Exception as e:
            if self._iptal:
                raise DownloadCancelledError("İndirme iptal edildi.") from e
            mesaj = str(e).strip() or "Bilinmeyen hata"
            if len(mesaj) > 120:
                mesaj = mesaj[:117] + "..."
            raise DownloadError(mesaj) from e
