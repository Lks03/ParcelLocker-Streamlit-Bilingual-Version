@echo off
cd /d "%~dp0"
python -m pip install -r requirements.txt
if errorlevel 1 goto failed
python -m streamlit run app.py
if errorlevel 1 goto failed
exit /b 0
:failed
echo.
echo Could not start. Check Python installation and the error above.
pause
exit /b 1
