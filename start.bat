@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ============================================================
echo   SSI - Smart Student Integrated
echo   Sadat Academy for Management Sciences
echo ============================================================
echo.

REM ---------- Backend ----------
echo [1/4] Preparing backend...
cd backend

if not exist "..\venv" (
    echo   - Creating virtual environment...
    python -m venv ..\venv
    if errorlevel 1 (
        echo   X Failed to create venv. Is Python installed and on PATH?
        pause
        exit /b 1
    )
)

call ..\venv\Scripts\activate.bat

echo   - Installing Python dependencies...
python -m pip install --upgrade pip >nul
pip install -r ..\requirements.txt
if errorlevel 1 (
    echo   X Failed to install Python dependencies.
    pause
    exit /b 1
)

cd ..

REM ---------- Seed DB ----------
echo [2/4] Checking database...
if not exist "database\ssi.db" (
    echo   - Seeding database from CSVs...
    call venv\Scripts\activate.bat
    python database\seed.py
    if errorlevel 1 (
        echo   X Database seeding failed.
        pause
        exit /b 1
    )
) else (
    echo   - Database already exists, skipping seed.
)

REM ---------- Frontend ----------
echo [3/4] Preparing frontend...
cd frontend

if not exist "node_modules" (
    echo   - Installing npm dependencies...
    call npm install
    if errorlevel 1 (
        echo   X Failed to install npm dependencies. Is Node.js installed?
        pause
        exit /b 1
    )
) else (
    echo   - node_modules already exists, skipping install.
)

cd ..

REM ---------- Launch ----------
echo [4/4] Starting servers...
echo.

start "SSI Backend" cmd /k "cd /d %~dp0backend && call ..\venv\Scripts\activate.bat && uvicorn main:app --reload --host 127.0.0.1 --port 8000"

start "SSI Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

timeout /t 6 >nul

echo.
echo ============================================================
echo   SSI is running:
echo     Backend  -^> http://127.0.0.1:8000
echo     API Docs -^> http://127.0.0.1:8000/docs
echo     Frontend -^> http://localhost:5173
echo ============================================================
echo.
echo Opening browser...
start http://localhost:5173

endlocal
