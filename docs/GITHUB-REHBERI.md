# İlk kez GitHub’da repo paylaşma rehberi

Bu rehber, **yt-dlp-gui** projesini GitHub’a ilk defa yüklemen için yazıldı. Adımları sırayla takip etmen yeterli.

---

## 1. Hazırlık (bilgisayarında)

### Git kurulu mu?

PowerShell’de:

```powershell
git --version
```

Hata alırsan: [https://git-scm.com/download/win](https://git-scm.com/download/win) → kur → terminali yeniden aç.

**Git kurmak istemezsen:** [GitHub Desktop](https://desktop.github.com/) indir → **File → Add local repository** → proje klasörünü seç → **Publish repository**. Aşağıdaki terminal adımlarının çoğu Desktop arayüzünde karşılığı var.

### GitHub hesabı

[https://github.com/signup](https://github.com/signup) ile ücretsiz hesap aç.

---

## 2. Repoya girmemesi gereken dosyalar

`.gitignore` şunları zaten dışarıda bırakır:

- `config.json` — senin klasör ayarın
- `indirme_gecmisi.json` — indirme geçmişin
- `.venv/` — sanal ortam
- İndirdiğin `.mp4` / `.mp3` dosyaları

**Asla yükleme:** şifre, API anahtarı, `cookies.txt` (varsa).

Kontrol için proje klasöründe:

```powershell
cd "C:\Users\efebs\OneDrive\Masaüstü\yt-dlp-gui"
git status
```

Kırmızı listede `config.json` görünmemeli (.gitignore sayesinde).

---

## 3. İlk commit (yerel Git)

Proje klasöründe:

```powershell
cd "C:\Users\efebs\OneDrive\Masaüstü\yt-dlp-gui"

git init

git add .

git status
```

`git status` çıktısında `assets/fonts/*.ttf` ve `.py` dosyaları **staged** olmalı; `config.json` olmamalı.

İlk commit:

```powershell
git commit -m "İlk sürüm: yt-dlp GUI masaüstü indirici"
```

---

## 4. GitHub’da boş repo oluştur

1. GitHub’da sağ üst **+** → **New repository**
2. **Repository name:** `yt-dlp-gui` (veya istediğin isim)
3. **Public** seç (açık kaynak için)
4. **Önemli:** “Add a README” ve “Add .gitignore” kutularını **işaretleme** — zaten projende var
5. **Create repository**

---

## 5. Kodu GitHub’a gönder (push)

GitHub sana komutlar gösterir. Örnek (kullanıcı adını değiştir):

```powershell
git branch -M main

git remote add origin https://github.com/KULLANICI_ADIN/yt-dlp-gui.git

git push -u origin main
```

İlk push’ta GitHub girişi isteyebilir:

- **Tarayıcı ile oturum** (önerilen), veya
- **Personal Access Token** — Settings → Developer settings → Tokens → `repo` yetkisi

---

## 6. README’yi kişiselleştir

`README.md` içinde şunları kendi bilginle değiştir:

- `KULLANICI_ADIN` → GitHub kullanıcı adın (2 yerde)
- İstersen `LICENSE` dosyasında `yt-dlp-gui contributors` → kendi adın

Değiştirdikten sonra:

```powershell
git add README.md LICENSE
git commit -m "README ve lisans kişiselleştirildi"
git push
```

---

## 7. Repo sayfasını güzel gösterme (isteğe bağlı)

| Ne | Nasıl |
|----|--------|
| **Açıklama** | Repo sayfası → dişli ⚙ → Description: “yt-dlp için masaüstü arayüz” |
| **Konular** | About → Topics: `python`, `yt-dlp`, `gui`, `customtkinter` |
| **Ekran görüntüsü** | `docs/screenshots/app.png` ekle, README’deki önizleme satırını aç |
| **Release** | Releases → Create new tag `v0.1.0` — “İlk public sürüm” notu |

---

## 8. Sonraki güncellemeler

Kod değiştirdikçe:

```powershell
git add .
git commit -m "Kısa açıklama: ne değişti"
git push
```

---

## Sık sorulan sorular

**“Repository not found”**  
→ `git remote -v` adresini kontrol et; repo adı ve kullanıcı adı doğru mu?

**“Permission denied”**  
→ Token veya GitHub Desktop ile tekrar giriş yap.

**Yanlışlıkla `config.json` yükledim**  
```powershell
git rm --cached config.json
git commit -m "config.json repodan çıkarıldı"
git push
```

**Repo ismini değiştirdim**  
GitHub → Settings → Repository name; yerelde:
```powershell
git remote set-url origin https://github.com/KULLANICI_ADIN/YENI-ISIM.git
```

---

## Kısa kontrol listesi

- [ ] `git init` ve ilk `commit` yapıldı
- [ ] GitHub’da boş repo oluşturuldu (README eklenmedi)
- [ ] `git push` başarılı
- [ ] README’deki `KULLANICI_ADIN` güncellendi
- [ ] `config.json` / geçmiş dosyası repoda yok
- [ ] İsteğe bağlı: ekran görüntüsü ve Topics eklendi

Takıldığın adımı Issue olarak da yazabilirsin — bu rehberi geliştirmek için faydalı olur.
