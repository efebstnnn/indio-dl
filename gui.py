import os
import threading

import customtkinter as ctk
from tkinter import filedialog

import config
import fonts
from downloader import DownloadCancelledError, DownloadError, VideoDownloader
from theme import Tema, bolum_etiketi


class DownloaderApp(ctk.CTk):
    KUYRUK_PLACEHOLDER = "Her satıra bir adres — toplu ekleme için"

    def __init__(self):
        super().__init__()

        self.downloader = VideoDownloader(progress_callback=self.arayuz_ilerleme_guncelle)
        self._bilgi_calisiyor = False
        self._indirme_calisiyor = False
        self.son_cekilen_baslik = ""
        self.kuyruk: list[dict] = []
        self._kuyruk_placeholder_aktif = True

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        fonts.yukle()
        Tema.guncelle_fontlar()

        self.configure(fg_color=Tema.BG)
        self.geometry("920x640")
        self.title("İndirici")
        self.resizable(True, True)
        self.minsize(820, 580)

        self.arayuz_tasarla()
        self._kayitli_ayarlari_yukle()
        self.gecmis_listesini_yenile()
        self.kuyruk_listesini_yenile()

    def _ui(self, fn):
        self.after(0, fn)

    def _btn_primary(self, parent, text, command, width=140, height=40):
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            width=width,
            height=height,
            font=Tema.FONT_BTN_PRIMARY,
            fg_color=Tema.ACCENT,
            hover_color=Tema.ACCENT_HOVER,
            text_color="#1a1510",
            corner_radius=Tema.RADIUS_SM,
        )

    def _btn_secondary(self, parent, text, command, width=120, height=34):
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            width=width,
            height=height,
            font=Tema.FONT_BTN,
            fg_color=Tema.BTN_SECONDARY,
            hover_color=Tema.BTN_SECONDARY_HOVER,
            text_color=Tema.TEXT,
            corner_radius=Tema.RADIUS_SM,
        )

    def _btn_ghost(self, parent, text, command, width=100, height=32):
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            width=width,
            height=height,
            font=Tema.FONT_SM,
            fg_color="transparent",
            hover_color=Tema.BTN_GHOST_HOVER,
            text_color=Tema.TEXT_SECONDARY,
            border_width=1,
            border_color=Tema.BORDER,
            corner_radius=Tema.RADIUS_SM,
        )

    def _btn_danger(self, parent, text, command, width=72, height=32):
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            width=width,
            height=height,
            font=Tema.FONT_SM,
            fg_color="transparent",
            hover_color="#3a2828",
            text_color=Tema.ERR,
            border_width=1,
            border_color=Tema.BORDER,
            corner_radius=Tema.RADIUS_SM,
        )

    def _kart(self, parent, height=64):
        return ctk.CTkFrame(
            parent,
            fg_color=Tema.SURFACE_ELEVATED,
            corner_radius=Tema.RADIUS_SM,
            border_width=1,
            border_color=Tema.BORDER,
            height=height,
        )

    def _kayitli_ayarlari_yukle(self):
        ayarlar = config.yukle()
        klasor = ayarlar.get("indirme_klasoru", "")
        if klasor and os.path.isdir(klasor):
            self.downloader.klasor_set(klasor)
            self._klasor_etiketini_guncelle(klasor)

    def _klasor_etiketini_guncelle(self, dizin: str):
        kisa = dizin if len(dizin) < 42 else f"…{dizin[-39:]}"
        self.klasor_label.configure(text=kisa, text_color=Tema.TEXT_SECONDARY)

    def _mevcut_indirme_ayarlari(self) -> tuple[str, str, str]:
        url = self.url_entry.get().strip()
        f_secim = self.format_menu.get()
        k_secim = "Ses" if f_secim == "MP3" else self.kalite_menu.get()
        return url, f_secim, k_secim

    def _kuyruk_metnini_al(self) -> str:
        if self._kuyruk_placeholder_aktif:
            return ""
        return self.kuyruk_metin.get("1.0", "end").strip()

    def _kuyruk_placeholder_goster(self):
        self._kuyruk_placeholder_aktif = True
        self.kuyruk_metin.delete("1.0", "end")
        self.kuyruk_metin.insert("1.0", self.KUYRUK_PLACEHOLDER)
        self.kuyruk_metin.configure(text_color=Tema.TEXT_DIM)

    def _kuyruk_placeholder_temizle(self, _event=None):
        if self._kuyruk_placeholder_aktif:
            self._kuyruk_placeholder_aktif = False
            self.kuyruk_metin.delete("1.0", "end")
            self.kuyruk_metin.configure(text_color=Tema.TEXT)

    def arayuz_tasarla(self):
        # —— Sol: indirme akışı ——
        self.sol_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.sol_frame.pack(side="left", fill="both", expand=True, padx=(28, 12), pady=24)

        ctk.CTkLabel(
            self.sol_frame,
            text="İndirici",
            font=Tema.FONT_TITLE,
            text_color=Tema.TEXT,
            anchor="w",
        ).pack(fill="x")

        ctk.CTkLabel(
            self.sol_frame,
            text="Bağlantıyı yapıştır, formatı seç, indir.",
            font=Tema.FONT_SM,
            text_color=Tema.TEXT_DIM,
            anchor="w",
        ).pack(fill="x", pady=(2, 20))

        bolum_etiketi(self.sol_frame, "Bağlantı").pack(fill="x", pady=(0, 6))
        self.url_entry = ctk.CTkEntry(
            self.sol_frame,
            placeholder_text="https://…",
            height=40,
            font=Tema.FONT,
            fg_color=Tema.INPUT,
            border_color=Tema.INPUT_BORDER,
            text_color=Tema.TEXT,
            placeholder_text_color=Tema.TEXT_DIM,
            corner_radius=Tema.RADIUS_SM,
        )
        self.url_entry.pack(fill="x", pady=(0, 16))

        bolum_etiketi(self.sol_frame, "Toplu ekleme").pack(fill="x", pady=(0, 6))
        self.kuyruk_metin = ctk.CTkTextbox(
            self.sol_frame,
            height=72,
            font=Tema.FONT_SM,
            fg_color=Tema.INPUT,
            border_color=Tema.INPUT_BORDER,
            text_color=Tema.TEXT,
            corner_radius=Tema.RADIUS_SM,
        )
        self.kuyruk_metin.pack(fill="x", pady=(0, 8))
        self.kuyruk_metin.bind("<FocusIn>", self._kuyruk_placeholder_temizle)
        self.kuyruk_metin.bind("<FocusOut>", self._kuyruk_placeholder_blur)
        self._kuyruk_placeholder_goster()

        kuyruk_satir = ctk.CTkFrame(self.sol_frame, fg_color="transparent")
        kuyruk_satir.pack(fill="x", pady=(0, 20))
        self._btn_ghost(kuyruk_satir, "Ekle", self.kuyruga_ekle, 72).pack(side="left", padx=(0, 6))
        self._btn_ghost(kuyruk_satir, "Metinden al", self.metinden_kuyruga_ekle, 100).pack(
            side="left", padx=(0, 6)
        )
        self._btn_ghost(kuyruk_satir, "Temizle", self.kuyrugu_temizle, 80).pack(side="left")

        self.btn_bilgi = self._btn_secondary(
            self.sol_frame, "Videoyu incele", self.bilgi_getir_tetikle, 140, 36
        )
        self.btn_bilgi.pack(anchor="w", pady=(0, 12))

        self.info_frame = ctk.CTkFrame(
            self.sol_frame,
            fg_color=Tema.SURFACE,
            corner_radius=Tema.RADIUS_SM,
            border_width=1,
            border_color=Tema.BORDER,
        )
        self.bilgi_label = ctk.CTkLabel(
            self.info_frame,
            text="Henüz video seçilmedi.",
            justify="left",
            font=Tema.FONT_SM,
            text_color=Tema.TEXT_SECONDARY,
            wraplength=360,
        )
        self.bilgi_label.pack(padx=16, pady=14, anchor="w")
        self.info_frame.pack(fill="x", pady=(0, 4))

        bolum_etiketi(self.sol_frame, "Çıktı").pack(fill="x", pady=(16, 8))

        self.select_frame = ctk.CTkFrame(self.sol_frame, fg_color="transparent")
        self.select_frame.pack(fill="x", pady=(0, 12))

        self.format_menu = ctk.CTkOptionMenu(
            self.select_frame,
            values=["MP4", "MP3"],
            width=100,
            height=36,
            font=Tema.FONT_SM,
            fg_color=Tema.INPUT,
            button_color=Tema.BTN_SECONDARY,
            button_hover_color=Tema.BTN_SECONDARY_HOVER,
            dropdown_fg_color=Tema.SURFACE_ELEVATED,
            command=self.format_degisti,
            corner_radius=Tema.RADIUS_SM,
        )
        self.format_menu.pack(side="left", padx=(0, 8))

        self.kalite_menu = ctk.CTkOptionMenu(
            self.select_frame,
            values=["En iyi"],
            width=110,
            height=36,
            font=Tema.FONT_SM,
            fg_color=Tema.INPUT,
            button_color=Tema.BTN_SECONDARY,
            button_hover_color=Tema.BTN_SECONDARY_HOVER,
            dropdown_fg_color=Tema.SURFACE_ELEVATED,
            corner_radius=Tema.RADIUS_SM,
        )
        self.kalite_menu.pack(side="left")

        klasor_satir = ctk.CTkFrame(self.sol_frame, fg_color="transparent")
        klasor_satir.pack(fill="x", pady=(0, 4))
        self._btn_ghost(klasor_satir, "Klasör", self.klasor_sec, 80).pack(side="left")
        self.klasor_label = ctk.CTkLabel(
            klasor_satir,
            text="Varsayılan konum",
            font=Tema.FONT_XS,
            text_color=Tema.TEXT_DIM,
            anchor="w",
        )
        self.klasor_label.pack(side="left", padx=(10, 0))

        self.indir_btn_frame = ctk.CTkFrame(self.sol_frame, fg_color="transparent")
        self.indir_btn_frame.pack(fill="x", pady=(20, 0))

        self.button = self._btn_primary(
            self.indir_btn_frame,
            "İndir",
            lambda: self.indir_tetikle(kuyruk_dahil=False),
            120,
            44,
        )
        self.button.pack(side="left", padx=(0, 10))

        self.btn_kuyruk_indir = self._btn_secondary(
            self.indir_btn_frame,
            "Kuyruğu indir",
            lambda: self.indir_tetikle(kuyruk_dahil=True),
            130,
            44,
        )
        self.btn_kuyruk_indir.pack(side="left")

        self.btn_iptal = self._btn_danger(
            self.sol_frame, "Durdur", self.indirmeyi_iptal_et, 90, 36
        )

        self.progress_bar = ctk.CTkProgressBar(
            self.sol_frame,
            height=6,
            progress_color=Tema.ACCENT,
            fg_color=Tema.BORDER,
            corner_radius=4,
        )
        self.progress_bar.set(0)

        self.durum_label = ctk.CTkLabel(
            self.sol_frame, text="", font=Tema.FONT_SM, text_color=Tema.TEXT_SECONDARY
        )
        self.durum_label.pack(fill="x", pady=(12, 0))

        self.btn_klasor_ac = self._btn_ghost(
            self.sol_frame, "İndirilenleri aç", self.downloader.klasoru_ac, 130, 34
        )

        # —— Sağ: geçmiş ve kuyruk ——
        self.sag_frame = ctk.CTkFrame(
            self,
            fg_color=Tema.SURFACE,
            corner_radius=Tema.RADIUS,
            border_width=1,
            border_color=Tema.BORDER,
            width=360,
        )
        self.sag_frame.pack(side="right", fill="both", padx=(12, 28), pady=24)
        self.sag_frame.pack_propagate(False)

        self.sag_tab = ctk.CTkTabview(
            self.sag_frame,
            fg_color="transparent",
            segmented_button_fg_color=Tema.INPUT,
            segmented_button_selected_color=Tema.ACCENT_MUTED,
            segmented_button_selected_hover_color=Tema.ACCENT_MUTED,
            segmented_button_unselected_color=Tema.INPUT,
            segmented_button_unselected_hover_color=Tema.BTN_SECONDARY,
            text_color=Tema.TEXT_SECONDARY,
            text_color_disabled=Tema.TEXT_DIM,
        )
        self.sag_tab.pack(fill="both", expand=True, padx=12, pady=12)
        self.sag_tab.add("Geçmiş")
        self.sag_tab.add("Kuyruk")
        self.sag_tab._segmented_button.configure(font=Tema.FONT_SM)

        self.gecmis_scroll = ctk.CTkScrollableFrame(
            self.sag_tab.tab("Geçmiş"),
            fg_color="transparent",
            scrollbar_button_color=Tema.BTN_SECONDARY,
        )
        self.gecmis_scroll.pack(fill="both", expand=True)

        self.kuyruk_scroll = ctk.CTkScrollableFrame(
            self.sag_tab.tab("Kuyruk"),
            fg_color="transparent",
            scrollbar_button_color=Tema.BTN_SECONDARY,
        )
        self.kuyruk_scroll.pack(fill="both", expand=True)

    def _kuyruk_placeholder_blur(self, _event=None):
        if not self.kuyruk_metin.get("1.0", "end").strip():
            self._kuyruk_placeholder_goster()

    def _durum_guncelle(self, metin: str, renk: str):
        self._ui(lambda: self.durum_label.configure(text=metin, text_color=renk))

    def _indirme_arayuzunu_ac(self):
        self.button.configure(state="disabled")
        self.btn_kuyruk_indir.configure(state="disabled")
        self.btn_bilgi.configure(state="disabled")
        self.btn_klasor_ac.pack_forget()
        self.btn_iptal.pack(pady=(16, 0), anchor="w")
        self.progress_bar.pack(fill="x", pady=(12, 0))
        self.progress_bar.set(0)

    def _indirme_arayuzunu_kapat(self):
        self.progress_bar.pack_forget()
        self.btn_iptal.pack_forget()
        self.button.configure(state="normal")
        self.btn_kuyruk_indir.configure(state="normal")
        self.btn_bilgi.configure(state="normal")

    def _butonlari_kilitle(self, kilitli: bool):
        durum = "disabled" if kilitli else "normal"
        self._ui(
            lambda: (
                self.button.configure(state=durum),
                self.btn_kuyruk_indir.configure(state=durum),
                self.btn_bilgi.configure(state=durum),
            )
        )

    def indirmeyi_iptal_et(self):
        self.downloader.iptal_talep_et()
        self._durum_guncelle("Durduruluyor…", Tema.WARN)

    def kuyruga_ekle(self):
        url, f_secim, k_secim = self._mevcut_indirme_ayarlari()
        if not url:
            self._durum_guncelle("Önce bir bağlantı girin.", Tema.ERR)
            return

        fmt = f"MP3" if f_secim == "MP3" else "MP4"
        baslik = self.son_cekilen_baslik or url[:48]
        self.kuyruk.append(
            {"url": url, "format": fmt, "kalite": k_secim, "baslik": baslik}
        )
        self.kuyruk_listesini_yenile()
        self.sag_tab.set("Kuyruk")
        self._durum_guncelle(f"Kuyrukta {len(self.kuyruk)} öğe.", Tema.TEXT_SECONDARY)

    def metinden_kuyruga_ekle(self):
        metin = self._kuyruk_metnini_al()
        if not metin:
            self._durum_guncelle("En az bir adres yazın.", Tema.ERR)
            return

        _, f_secim, k_secim = self._mevcut_indirme_ayarlari()
        fmt = "MP3" if f_secim == "MP3" else "MP4"
        eklenen = 0
        for satir in metin.splitlines():
            url = satir.strip()
            if url.startswith(("http://", "https://")):
                self.kuyruk.append(
                    {
                        "url": url,
                        "format": fmt,
                        "kalite": k_secim,
                        "baslik": url[:48],
                    }
                )
                eklenen += 1

        if eklenen == 0:
            self._durum_guncelle("Geçerli bir http adresi bulunamadı.", Tema.ERR)
            return

        self.kuyruk_listesini_yenile()
        self.sag_tab.set("Kuyruk")
        self._durum_guncelle(f"{eklenen} adres eklendi.", Tema.TEXT_SECONDARY)

    def kuyrugu_temizle(self):
        self.kuyruk.clear()
        self.kuyruk_listesini_yenile()
        self._durum_guncelle("Kuyruk boşaltıldı.", Tema.TEXT_DIM)

    def kuyruk_listesini_yenile(self):
        def yenile():
            for widget in self.kuyruk_scroll.winfo_children():
                widget.destroy()

            if not self.kuyruk:
                ctk.CTkLabel(
                    self.kuyruk_scroll,
                    text="Henüz bir şey yok.\nÜstten ekleyebilirsin.",
                    text_color=Tema.TEXT_DIM,
                    font=Tema.FONT_SM,
                    justify="left",
                ).pack(pady=24, padx=8, anchor="w")
                self.btn_kuyruk_indir.configure(text="Kuyruğu indir", state="disabled")
                return

            n = len(self.kuyruk)
            self.btn_kuyruk_indir.configure(text=f"Kuyruğu indir ({n})", state="normal")

            for i, item in enumerate(self.kuyruk):
                kart = self._kart(self.kuyruk_scroll, 56)
                kart.pack(fill="x", pady=3, padx=2)
                kart.pack_propagate(False)

                baslik = item.get("baslik", item["url"])
                kisa = baslik if len(baslik) < 32 else f"{baslik[:29]}…"

                ust = ctk.CTkFrame(kart, fg_color="transparent")
                ust.pack(fill="x", padx=12, pady=(8, 2))

                ctk.CTkLabel(
                    ust,
                    text=kisa,
                    font=Tema.FONT_SM,
                    text_color=Tema.TEXT,
                    anchor="w",
                ).pack(side="left", fill="x", expand=True)

                self._btn_ghost(
                    ust, "Kaldır", lambda idx=i: self.kuyruktan_sil(idx), 64, 26
                ).pack(side="right")

                fmt = item.get("format", "?")
                kal = item.get("kalite", "?")
                ctk.CTkLabel(
                    kart,
                    text=f"{fmt} · {kal}",
                    font=Tema.FONT_XS,
                    text_color=Tema.TEXT_DIM,
                    anchor="w",
                ).pack(fill="x", padx=12, pady=(0, 8))

        self._ui(yenile)

    def kuyruktan_sil(self, index: int):
        if 0 <= index < len(self.kuyruk):
            self.kuyruk.pop(index)
            self.kuyruk_listesini_yenile()

    def gecmis_listesini_yenile(self):
        def yenile():
            for widget in self.gecmis_scroll.winfo_children():
                widget.destroy()

            gecmis_verileri = self.downloader.gecmisi_yukle()
            if not gecmis_verileri:
                ctk.CTkLabel(
                    self.gecmis_scroll,
                    text="İlk indirmeden sonra\nburada görünür.",
                    text_color=Tema.TEXT_DIM,
                    font=Tema.FONT_SM,
                    justify="left",
                ).pack(pady=24, padx=8, anchor="w")
                return

            for item in gecmis_verileri:
                kart = self._kart(self.gecmis_scroll, 68)
                kart.pack(fill="x", pady=3, padx=2)
                kart.pack_propagate(False)

                baslik = item.get("baslik", "Bilinmeyen")
                kisa = baslik if len(baslik) < 30 else f"{baslik[:27]}…"

                ust = ctk.CTkFrame(kart, fg_color="transparent")
                ust.pack(fill="x", padx=12, pady=(10, 2))

                ctk.CTkLabel(
                    ust, text=kisa, font=Tema.FONT_SM, text_color=Tema.TEXT, anchor="w"
                ).pack(side="left", fill="x", expand=True)

                url = item.get("url", "")
                if url:
                    self._btn_ghost(
                        ust, "Yükle", lambda u=url: self.gecmisten_kullan(u), 64, 26
                    ).pack(side="right")

                fmt = item.get("format", "?").replace(" (Video)", "").replace(" (Ses)", "")
                if "MP" not in fmt:
                    fmt = fmt[:6]
                ctk.CTkLabel(
                    kart,
                    text=f"{fmt} · {item.get('kalite', '?')} · {item.get('tarih', '')}",
                    font=Tema.FONT_XS,
                    text_color=Tema.TEXT_DIM,
                    anchor="w",
                ).pack(fill="x", padx=12, pady=(0, 10))

        self._ui(yenile)

    def gecmisten_kullan(self, url: str):
        self.url_entry.delete(0, "end")
        self.url_entry.insert(0, url)
        self.bilgi_getir_tetikle()

    def format_degisti(self, secilen_format):
        if secilen_format == "MP3":
            self.kalite_menu.pack_forget()
        else:
            self.kalite_menu.pack(side="left")

    def klasor_sec(self):
        dizin = filedialog.askdirectory()
        if dizin:
            self.downloader.klasor_set(dizin)
            config.kaydet(dizin)
            self._klasor_etiketini_guncelle(dizin)

    def bilgi_getir_tetikle(self):
        if self._bilgi_calisiyor or self._indirme_calisiyor:
            return
        threading.Thread(target=self.bilgi_getir_islemi, daemon=True).start()

    def bilgi_getir_islemi(self):
        self._bilgi_calisiyor = True
        self._butonlari_kilitle(True)

        url = self.url_entry.get().strip()
        if not url:
            self._durum_guncelle("Önce bir bağlantı girin.", Tema.ERR)
            self._bilgi_calisiyor = False
            self._butonlari_kilitle(False)
            return

        self._durum_guncelle("Video bilgisi alınıyor…", Tema.TEXT_SECONDARY)
        sonuc = self.downloader.bilgi_ve_kalite_cek(url)

        def sonucu_uygula():
            if sonuc["hata"]:
                hata = sonuc["hata"]
                if len(hata) > 72:
                    hata = hata[:69] + "…"
                self.bilgi_label.configure(
                    text=f"Alınamadı: {hata}",
                    text_color=Tema.ERR,
                )
                self.indir_btn_frame.pack_forget()
            else:
                self.son_cekilen_baslik = sonuc["baslik"]
                max_k = sonuc["kaliteler"][0] if sonuc["kaliteler"] else "—"
                kisa = (
                    self.son_cekilen_baslik
                    if len(self.son_cekilen_baslik) < 48
                    else f"{self.son_cekilen_baslik[:45]}…"
                )
                self.bilgi_label.configure(
                    text=f"{kisa}\nEn yüksek: {max_k}",
                    text_color=Tema.TEXT,
                )

                if sonuc["kaliteler"]:
                    self.kalite_menu.configure(values=sonuc["kaliteler"])
                    self.kalite_menu.set(sonuc["kaliteler"][0])
                else:
                    self.kalite_menu.configure(values=["En iyi"])
                    self.kalite_menu.set("En iyi")

                if not self.indir_btn_frame.winfo_ismapped():
                    self.indir_btn_frame.pack(fill="x", pady=(20, 0))

                self._durum_guncelle("Hazır — indirebilirsin.", Tema.OK)

            self._bilgi_calisiyor = False
            self._butonlari_kilitle(False)

        self._ui(sonucu_uygula)

    def arayuz_ilerleme_guncelle(self, yuzde, hiz, sure):
        def guncelle():
            try:
                oran = min(1.0, max(0.0, float(yuzde) / 100))
                self.progress_bar.set(oran)
                mevcut = self.durum_label.cget("text")
                if "İndiriliyor" in mevcut or "indiriliyor" in mevcut.lower():
                    parca = mevcut.split("·", 1)[0].strip().rstrip("—").strip()
                    if not parca.endswith("—"):
                        parca = parca.split(":")[0].strip()
                    self.durum_label.configure(
                        text=f"{parca} — %{yuzde} · {hiz} · {sure} kaldı",
                        text_color=Tema.ACCENT,
                    )
            except ValueError:
                pass

        self._ui(guncelle)

    def indir_tetikle(self, kuyruk_dahil: bool = False):
        if self._bilgi_calisiyor or self._indirme_calisiyor:
            return
        threading.Thread(
            target=self.indir_islemi, args=(kuyruk_dahil,), daemon=True
        ).start()

    def _indirme_listesi_olustur(self, kuyruk_dahil: bool) -> list[dict]:
        url, f_secim, k_secim = self._mevcut_indirme_ayarlari()
        liste = []
        fmt = "MP3" if f_secim == "MP3" else "MP4"
        fmt_indir = "MP3 (Ses)" if f_secim == "MP3" else "MP4 (Video)"

        if kuyruk_dahil:
            for oge in self.kuyruk:
                f = oge.get("format", "MP4")
                liste.append(
                    {
                        "url": oge["url"],
                        "format": "MP3 (Ses)" if f == "MP3" else "MP4 (Video)",
                        "kalite": oge["kalite"],
                        "baslik": oge.get("baslik", ""),
                    }
                )
            self.kuyruk.clear()
            self._ui(self.kuyruk_listesini_yenile)
        elif url:
            liste.append(
                {
                    "url": url,
                    "format": fmt_indir,
                    "kalite": k_secim,
                    "baslik": self.son_cekilen_baslik or url[:48],
                }
            )

        return liste

    def indir_islemi(self, kuyruk_dahil: bool):
        self._indirme_calisiyor = True
        self.downloader.iptal_sifirla()

        indirmeler = self._indirme_listesi_olustur(kuyruk_dahil)
        if not indirmeler:
            mesaj = (
                "Kuyruk boş — önce bir şey ekle."
                if kuyruk_dahil
                else "Önce bir bağlantı girin."
            )
            self._durum_guncelle(mesaj, Tema.ERR)
            self._indirme_calisiyor = False
            return

        self._ui(self._indirme_arayuzunu_ac)

        toplam = len(indirmeler)
        basarili = 0
        iptal = False

        try:
            for sira, oge in enumerate(indirmeler, start=1):
                if self.downloader.iptal_edildi_mi():
                    iptal = True
                    break

                url = oge["url"]
                f_secim = oge["format"]
                k_secim = oge["kalite"]
                baslik = oge.get("baslik", "")
                gecmis_fmt = "MP3" if "MP3" in f_secim else "MP4"

                etiket = baslik if len(baslik) < 36 else f"{baslik[:33]}…"
                self._durum_guncelle(
                    f"İndiriliyor ({sira}/{toplam}) — {etiket}", Tema.ACCENT
                )
                self._ui(lambda: self.progress_bar.set(0))

                try:
                    indirilen_baslik = self.downloader.indir(url, f_secim, k_secim)
                    if not baslik or baslik == url[:48]:
                        baslik = indirilen_baslik

                    self.downloader.gecmise_ekle(baslik, k_secim, gecmis_fmt, url)
                    basarili += 1
                except DownloadCancelledError:
                    iptal = True
                    break
                except DownloadError as e:
                    self._durum_guncelle(f"{sira}/{toplam} — {e}", Tema.ERR)
                    print(f"İndirme hatası [{url}]: {e}")
                    continue

            def bitir():
                self._indirme_arayuzunu_kapat()
                self.gecmis_listesini_yenile()

                if iptal:
                    self.durum_label.configure(
                        text=f"Durduruldu. {basarili} / {toplam} bitti.",
                        text_color=Tema.WARN,
                    )
                elif basarili == toplam:
                    self.durum_label.configure(
                        text=(
                            "Tamamlandı."
                            if toplam == 1
                            else f"{basarili} indirme tamamlandı."
                        ),
                        text_color=Tema.OK,
                    )
                    self.btn_klasor_ac.pack(anchor="w", pady=(12, 0))
                elif basarili > 0:
                    self.durum_label.configure(
                        text=f"{basarili} / {toplam} tamam — bazıları olmadı.",
                        text_color=Tema.WARN,
                    )
                    self.btn_klasor_ac.pack(anchor="w", pady=(12, 0))
                else:
                    self.durum_label.configure(
                        text="İndirme tamamlanamadı.", text_color=Tema.ERR
                    )

            self._ui(bitir)
        except Exception as e:
            def beklenmeyen():
                self._indirme_arayuzunu_kapat()
                self.durum_label.configure(
                    text="Beklenmeyen bir sorun oluştu.", text_color=Tema.ERR
                )

            self._ui(beklenmeyen)
            print(f"Beklenmeyen hata: {e}")
        finally:
            self.downloader.iptal_sifirla()
            self._indirme_calisiyor = False
