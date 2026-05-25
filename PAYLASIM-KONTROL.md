# Paylaşım öncesi kontrol listesi

Repoyu GitHub’a atmadan önce bu listeyi işaretle.

## Dosyalar

- [x] `README.md` — kurulum ve kullanım
- [x] `LICENSE` — MIT
- [x] `.gitignore` — `config.json`, geçmiş, medya dosyaları
- [x] `requirements.txt`
- [x] `assets/fonts/` — Inter fontları
- [x] `docs/GITHUB-REHBERI.md` — ilk repo rehberi
- [x] `.github/workflows/ci.yml` — otomatik derleme kontrolü

## Senin yapman gerekenler

- [ ] `README.md` ve `CONTRIBUTING.md` içinde `KULLANICI_ADIN` → GitHub kullanıcı adın
- [ ] `LICENSE` içinde isteğe bağlı: kendi adın
- [ ] `config.json` ve `indirme_gecmisi.json` commit’e **dahil değil** (`.gitignore`)
- [ ] İsteğe bağlı: `docs/screenshots/app.png` ekran görüntüsü
- [ ] Git veya GitHub Desktop kurulu
- [ ] GitHub’da repo oluşturuldu ve `git push` yapıldı

## Hızlı komutlar (Git kuruluysa)

```powershell
cd "C:\Users\efebs\OneDrive\Masaüstü\yt-dlp-gui"
git init
git add .
git commit -m "İlk sürüm: yt-dlp GUI"
git branch -M main
git remote add origin https://github.com/KULLANICI_ADIN/yt-dlp-gui.git
git push -u origin main
```

Detaylı anlatım: [docs/GITHUB-REHBERI.md](docs/GITHUB-REHBERI.md)
