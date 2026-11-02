@echo off
title FRESIC - Fruit and Vegetable Delivery
cd /d "%~dp0"
echo.
echo ==========================================
echo       FRESIC WEBSITE STARTER
echo ==========================================
echo.
where py >nul 2>nul
if %errorlevel%==0 (
    set PYTHON=py
) else (
    where python >nul 2>nul
    if %errorlevel%==0 (
        set PYTHON=python
    ) else (
        echo Python is not installed or not added to PATH.
        echo Please install Python from https://www.python.org/downloads/
        echo During installation, tick "Add Python to PATH".
        pause
        exit /b 1
    )
)
if not exist ".venv\Scripts\python.exe" (
    echo First-time setup: creating local environment...
    %PYTHON% -m venv .venv
    if errorlevel 1 goto error
)
echo Installing required packages...
".venv\Scripts\python.exe" -m pip install --disable-pip-version-check -r requirements.txt
if errorlevel 1 goto error
echo.
echo Starting FRESIC...
echo Keep this black window open while using the website.
echo Open http://127.0.0.1:5000 in your browser.
echo Admin dashboard: http://127.0.0.1:5000/admin/login
echo.
start "" http://127.0.0.1:5000
".venv\Scripts\python.exe" app.py
pause
exit /b 0
:error
echo.
echo Setup failed. Check that internet is available and Python is installed.
pause
exit /b 1
