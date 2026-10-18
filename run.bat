@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [Muse] Creation de l'environnement virtuel...
    py -3.12 -m venv .venv 2>nul || python -m venv .venv
    ".venv\Scripts\python.exe" -m pip install --upgrade pip
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt
)

echo [Muse] Application disponible sur http://localhost:8501
".venv\Scripts\python.exe" -m streamlit run app.py
