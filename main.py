import fonts
from gui import DownloaderApp
from theme import Tema

if __name__ == "__main__":
    fonts.yukle()
    Tema.guncelle_fontlar()
    app = DownloaderApp()
    app.mainloop()