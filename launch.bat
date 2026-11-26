@echo off
cd /d "%~dp0"
py -m pip install -r requirements.txt || exit /b 1
py -m streamlit run app.py --server.address 127.0.0.1
