#!/bin/bash

# Set color codes for better output
clear
echo "\033[34m🚀 YouTube Video Summarizer - Professional Setup\033[0m"
echo "\033[34m=====================================================\033[0m"
echo "\033[92m✨ AI-powered video summarization with Google Gemini\033[0m"
echo

# Check if Python is installed
echo "\033[93m📋 Checking system requirements...\033[0m"
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "\033[91m❌ Python not found. Please install Python 3.8+ first.\033[0m"
        echo "\033[93m📥 Download from: https://python.org/downloads/\033[0m"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# Get Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d" " -f2)
echo "\033[92m✅ Python $PYTHON_VERSION detected\033[0m"

# Check for virtual environment
if [ -f "venv/bin/activate" ]; then
    echo "\033[92m✅ Virtual environment found\033[0m"
    source venv/bin/activate
else
    echo "\033[93m📦 Creating virtual environment...\033[0m"
    $PYTHON_CMD -m venv venv
    source venv/bin/activate
    echo "\033[92m✅ Virtual environment created\033[0m"
fi

# Upgrade pip and install dependencies
echo "\033[93m📦 Installing dependencies...\033[0m"
python -m pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "\033[91m❌ Failed to install dependencies\033[0m"
    exit 1
else
    echo "\033[92m✅ Dependencies installed successfully\033[0m"
fi

echo
echo "\033[93m🔧 Checking configuration...\033[0m"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp ".env.example" ".env"
        echo "\033[93m📝 Created .env file from template\033[0m"
    else
        echo "GOOGLE_API_KEY=your_actual_google_api_key_here" > .env
        echo "\033[93m📝 Created .env file\033[0m"
    fi
fi

# Check if API key is configured
if grep -q "your_actual_api_key_here" .env; then
    echo "\033[91m⚠️  API key not configured!\033[0m"
    echo "\033[93m🔑 Please update your GOOGLE_API_KEY in .env file\033[0m"
    echo "\033[34m📖 Get your key from: https://aistudio.google.com/app/apikey\033[0m"
    echo
    echo "\033[93mOpening .env file for editing...\033[0m"
    
    # Try to open with default editor
    if command -v nano &> /dev/null; then
        nano .env
    elif command -v vim &> /dev/null; then
        vim .env
    elif command -v vi &> /dev/null; then
        vi .env
    else
        echo "\033[93mPlease edit .env file manually and press Enter when done...\033[0m"
        read -p "Press Enter to continue..."
    fi
fi

echo "\033[92m✅ Configuration complete\033[0m"
echo
echo "\033[34m🚀 Starting YouTube Video Summarizer...\033[0m"
echo "\033[93m📱 Opening in your default browser...\033[0m"
echo "\033[93m🌐 URL: http://localhost:8501\033[0m"
echo
echo "\033[92mPress Ctrl+C to stop the application\033[0m"
echo
streamlit run app.py --server.headless false

echo
echo "\033[93m👋 Application stopped. Thank you for using YouTube Video Summarizer!\033[0m"