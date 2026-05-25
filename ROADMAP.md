# yt-dlp-gui — Yol Haritası

Bu belge, projenin GitHub’da paylaşılabilir hale gelmesi ve sonrasında özellik geliştirmesi için önerilen sırayı tanımlar. Tarihler esnektir; her faz bitince bir sonrakine geçilmesi yeterlidir.

---

## Mevcut durum (v0.0)

| Var | Yok |
|-----|-----|
| Tek URL ile indirme | README, lisans, requirements |
| MP4 / MP3, kalite seçimi | İndirmeyi iptal etme |
| İlerleme çubuğu (%, hız, ETA) | Ayarları kalıcı kaydetme |
| İndirme geçmişi (JSON) | Geçmişte URL / tekrar indir |
| Klasör seçimi ve açma | Kuyruk / çoklu link |
| CustomTkinter karanlık arayüz | Altyazı, çerez, proxy |
| | Çoklu dil, paketlenmiş exe |

---

## Faz 1 — Paylaşıma hazırlık (v0.1)

**Hedef:** Repoyu klonlayan biri 5 dakikada çalıştırabilsin; temel dokümantasyon tam olsun.

### Depo ve dokümantasyon
- [ ] `README.md` — Proje tanımı, ekran görüntüsü, kurulum, kullanım, FFmpeg notu
- [ ] `requirements.txt` — `customtkinter`, `yt-dlp` (sürüm aralığı)
- [ ] `LICENSE` — MIT (veya seçtiğiniz lisans)
- [ ] `.gitignore` — `__pycache__/`, `*.pyc`, `indirme_gecmisi.json`, `config.json`, `.venv/`
- [ ] `CONTRIBUTING.md` (isteğe bağlı) — Issue / PR kısa rehberi

### Güvenilirlik
- [ ] Hata mesajlarını iyileştir — Kullanıcıya kısa Türkçe özet; teknik detay konsol / log
- [ ] FFmpeg kontrolü — MP3 seçildiğinde yoksa indirme başlamadan uyarı
- [ ] yt-dlp güncellik uyarısı — Açılışta veya hata sonrası “`pip install -U yt-dlp`” önerisi
- [ ] Çift tıklama / eşzamanlı indirme koruması — İndirme sırasında butonlar ve ikinci işlem engeli

### Yasal / etik (README içinde)
- [ ] Telif ve platform kullanım şartlarına uygun kullanım uyarısı
- [ ] “Yalnızca indirme hakkınız olan içerik” ifadesi

**Çıktı:** İlk public commit; “Works on my machine” yerine tekrarlanabilir kurulum.

---

## Faz 2 — Günlük kullanımı rahatlatma (v0.2)

**Hedef:** Tekrar açan kullanıcı için sürtünme azalsın; geçmiş gerçekten işe yarasın.

### Ayarlar
- [ ] `config.json` — Son indirme klasörü, varsayılan format (MP4/MP3), varsayılan kalite
- [ ] Uygulama açılışında ayarları yükle

### Geçmiş
- [ ] Geçmiş kaydına `url` alanı ekle
- [ ] Geçmiş kartında **Tekrar indir** — URL’yi alana doldur veya doğrudan indir
- [ ] Geçmişten tek kayıt silme / tüm geçmişi temizleme

### Arayüz
- [ ] Pencereyi yeniden boyutlandırılabilir yap (`resizable`)
- [ ] Dosya adı şablonu — MP3 ve MP4 için ayrı `outtmpl` (yükseklik yokken garip isimler düzeltilsin)
- [ ] Linki sürükle-bırak ile URL alanına yapıştırma

### Hata ayıklama
- [ ] Daraltılabilir **Log / detay** paneli veya pencere — Issue açanlar için

**Çıktı:** v0.2 tag; “günlük kullanılabilir” sürüm.

---

## Faz 3 — Güç kullanıcıları (v0.3)

**Hedef:** Playlist, kuyruk ve yt-dlp’nin gelişmiş seçeneklerine kapı arala.

### İndirme
- [ ] **İndirmeyi iptal et** — `YoutubeDL` işlemini thread + iptal bayrağı ile durdurma
- [ ] **Kuyruk** — Birden fazla URL (satır satır veya dosyadan); sırayla indirme
- [ ] Playlist URL desteği — Tüm liste veya “sadece bu video” seçeneği
- [ ] İndirme bitince isteğe bağlı **Windows bildirimi** (toast)

### İçerik seçenekleri
- [ ] **Altyazı** — Mevcut dilleri listele, SRT/VTT indir
- [ ] **Kapak görseli** — Thumbnail embed veya ayrı dosya
- [ ] **Çerez dosyası** — `cookies.txt` seçimi (giriş / yaş kısıtlı içerik)

### Bilgi önizleme
- [ ] Video bilgisi çekerken küçük **thumbnail**
- [ ] Seçilen kalite için yaklaşık **dosya boyutu** (mümkünse)

**Çıktı:** v0.3 tag; GitHub’da “feature-complete” indie indirici seviyesi.

---

## Faz 4 — Dağıtım ve topluluk (v1.0)

**Hedef:** Teknik olmayan kullanıcılar da deneyebilsin; proje sürdürülebilir olsun.

### Paketleme
- [ ] **PyInstaller** (veya benzeri) — Windows `.exe`; README’de FFmpeg kurulumu
- [ ] İsteğe bağlı: GitHub **Releases** ile exe ekleme

### Uluslararasılaştırma
- [ ] Arayüz metinleri için TR / EN (basit sözlük veya JSON)
- [ ] README İngilizce (veya TR + EN iki bölüm)

### Kalite
- [ ] `downloader.py` için birkaç **unit test** (mock `yt_dlp`)
- [ ] GitHub Actions — Lint + test (opsiyonel: sadece test)

### Gelecek (v1.x+)
- [ ] Proxy / kullanıcı aracısı ayarı
- [ ] Hız sınırı (`--limit-rate`)
- [ ] Sistem tepsisinde arka plan + kuyruk
- [ ] macOS / Linux klasör açma iyileştirmesi (zaten kısmen var)
- [ ] Otomatik yt-dlp güncelleme (dikkatli; kullanıcı onayı ile)

**Çıktı:** v1.0 tag; “paylaşılabilir ürün” hissi.

---

## Öncelik matrisi

| Öncelik | Öğe | Etki | Efor |
|--------|-----|------|------|
| P0 | README + requirements + lisans + .gitignore | Çok yüksek | Düşük |
| P0 | FFmpeg uyarısı, daha iyi hatalar | Yüksek | Düşük |
| P1 | config.json, geçmişte URL + tekrar indir | Yüksek | Orta |
| P1 | İndirmeyi iptal | Yüksek | Orta |
| P2 | Kuyruk / playlist | Orta–yüksek | Orta–yüksek |
| P2 | Altyazı, çerez | Orta | Orta |
| P3 | PyInstaller exe | Yüksek (yeni kitle) | Orta–yüksek |
| P3 | i18n, CI, test | Orta (güven) | Orta |

---

## Önerilen zaman çizelgesi (esnek)

```
Hafta 1–2   → Faz 1 (v0.1 public)
Hafta 3–4   → Faz 2 (v0.2)
Hafta 5–8   → Faz 3 (v0.3) — iptal + kuyruk en uzun parçalar
Hafta 9+    → Faz 4 (v1.0) — exe ve i18n
```

Hızınıza göre kaydırılabilir; Faz 1 bitmeden Faz 3’e geçmemek issue ve kullanıcı şikayetlerini azaltır.

---

## Sürüm etiketleme

| Tag | Anlam |
|-----|--------|
| `v0.1.0` | İlk public repo, dokümantasyon + stabilite yamaları |
| `v0.2.0` | Ayarlar + geçmiş iyileştirmeleri |
| `v0.3.0` | İptal, kuyruk, altyazı/çerez |
| `v1.0.0` | Exe dağıtımı + README EN + temel test/CI |

Küçük düzeltmeler: `v0.2.1`, `v0.3.2` vb.

---

## Takip

İlerledikçe bu dosyadaki `- [ ]` maddelerini `- [x]` yapabilirsiniz. İsterseniz GitHub **Projects** veya **Milestones** ile aynı fazları issue olarak açın (ör. `good first issue` → README, `.gitignore`).

---

*Son güncelleme: Mayıs 2026*
