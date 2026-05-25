import os
import sys

import fonts
from gui import DownloaderApp
from theme import Tema

if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

os.environ["PATH"] = BASE_DIR + os.pathsep + os.environ.get("PATH", "")

if __name__ == "__main__":
    fonts.yukle()
    Tema.guncelle_fontlar()
    app = DownloaderApp()
    app.mainloop()