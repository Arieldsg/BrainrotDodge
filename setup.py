from cx_Freeze import setup, Executable
import os

arquivos = [("Recursos", "Recursos")]

setup(
    name="BrainrotDodge",
    version="0.1",
    description="Seu jogo",
    
options={
    "build_exe": {
        "include_files": arquivos,
        "includes": [
            "aifc",
            "chunk",
            "audioop",
            "pyttsx3.drivers",
            "pyttsx3.drivers.sapi5"
        ],
    }
},

    executables=[Executable("main.py")]
)
