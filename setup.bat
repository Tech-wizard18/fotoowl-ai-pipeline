@echo off
REM Setup script for FotoOwl AI Pipeline (Windows)

echo 🦉 FotoOwl AI — Setup Script
echo ==============================
echo.

REM Check Python
echo Checking Python version...
python --version >nul 2>&1 || (
    echo Error: Python 3.11+ required
    exit /b 1
)

REM Check Node.js
echo Checking Node.js version...
node --version >nul 2>&1 || (
    echo Error: Node.js 18+ required
    exit /b 1
)

REM Create venv
echo.
echo Creating Python virtual environment...
python -m venv venv

REM Activate venv
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install Python deps
echo.
echo Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Install Node deps
echo.
echo Installing Remotion dependencies...
cd remotion
call npm install
cd ..

REM Create .env if missing
if not exist .env (
    echo.
    echo Creating .env file from template...
    copy .env.example .env
    echo ⚠️  Please edit .env and add your OPENAI_API_KEY
)

echo.
echo ✅ Setup complete!
echo.
echo Next steps:
echo   1. Edit .env and add your OPENAI_API_KEY
echo   2. Place images in sample_images\ folder
echo   3. Run: python main.py --images sample_images --prompt "Your creative prompt"
echo.
pause
