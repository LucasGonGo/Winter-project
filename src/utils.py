# utils.py
import os, sys, pathlib

def resource_path(rel_path: str) -> str:
    """
    Retorna caminho para recursos, funcionando nos três cenários:
    1) script normal (base = pasta do arquivo atual, ../)
    2) PyInstaller onedir (base = pasta que contém o .exe)
    3) PyInstaller onefile (base = _MEIPASS)
    """
    if hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS
    else:
        # pasta onde ESTE arquivo está (utils.py), depois sobe 1 nível
        base = pathlib.Path(__file__).resolve().parent.parent
    return os.path.join(base, rel_path)
