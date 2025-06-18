from cx_Freeze import setup, Executable
import sys
import os

build_exe_options = {
    "packages": ["pygame", "pyttsx3", "speech_recognition"],
    "include_files": [
        "Recursos/"
    ]
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Brainrot Dodge",
    version="1.0",
    description="Jogo desenvolvido com Python e Pygame",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base)]
)




