@echo off
setlocal EnableDelayedExpansion

cls
echo.
echo 🚀 YouTube Video Summarizer - Professional Setup
echo =====================================================
echo.
echo ✨ AI-powered video summarization with Google Gemini
echo.

:: Check if Python is installed
echo 📋 Checking system requirements...
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ Python not found. Please install Python 3.8+ first.
    echo 📥 Download from: https://python.org/downloads/
    pause
    exit /b 1
) else (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do echo ✅ Python %%i detected
)

:: Check for virtual environment
if exist "venv\Scripts\activate.bat" (
    echo ✅ Virtual environment found
    call venv\Scripts\activate.bat
) else (
    echo 📦 Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo ✅ Virtual environment created
)

echo.
echo 📦 Installing dependencies...
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
) else (
    echo ✅ Dependencies installed successfully
)

echo.
echo 🔧 Checking configuration...
if not exist ".env" (
    if exist ".env.example" (
        copy ".env.example" ".env" >nul
        echo 📝 Created .env file from template
    ) else (
        echo GOOGLE_API_KEY=your_actual_google_api_key_here > .env
        echo 📝 Created .env file
    )
)

:: Check if API key is configured
findstr /C:"your_actual_api_key_here" .env >nul
if %ERRORLEVEL% equ 0 (
    echo ⚠️  API key not configured!
    echo 🔑 Please update your GOOGLE_API_KEY in .env file
    echo 📖 Get your key from: https://aistudio.google.com/app/apikey
    echo.
    echo Opening .env file for editing...
    notepad .env
    pause
    echo Press any key after saving your API key...
    pause >nul
)

echo ✅ Configuration complete
echo.
echo 🚀 Starting YouTube Video Summarizer...
echo 📱 Opening in your default browser...
echo 🌐 URL: http://localhost:8501
echo.
echo Press Ctrl+C to stop the application
echo.
streamlit run app.py --server.headless false

echo.
echo 👋 Application stopped. Thank you for using YouTube Video Summarizer!
pause