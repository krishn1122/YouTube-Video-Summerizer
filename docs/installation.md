# Installation Guide

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 1GB free space
- **Internet**: Stable connection required

### Recommended Setup
- **Python**: 3.10 or 3.11 (latest stable)
- **Virtual Environment**: Recommended for isolation
- **Package Manager**: pip (latest version)

## Quick Installation

### Option 1: One-Click Setup (Recommended)

**For Windows Users:**
1. Download the project
2. Double-click `setup_and_run.bat`
3. Wait for automatic installation
4. Application will start automatically

**For Linux/Mac Users:**
1. Download the project
2. Open terminal in project directory
3. Run: `bash setup_and_run.sh`
4. Application will start automatically

### Option 2: Manual Installation

#### Step 1: Clone Repository
```bash
# Using Git
git clone https://github.com/yourusername/youtube-video-summarizer.git
cd youtube-video-summarizer

# Or download ZIP and extract
wget https://github.com/yourusername/youtube-video-summarizer/archive/main.zip
unzip main.zip
cd youtube-video-summarizer-main
```

#### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\\Scripts\\activate

# On Linux/Mac:
source venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install required packages
pip install -r requirements.txt
```

#### Step 4: Configure Environment
```bash
# Create .env file
cp .env.example .env  # Linux/Mac
copy .env.example .env  # Windows

# Edit .env file and add your Google API key
echo \"GOOGLE_API_KEY=your_actual_api_key_here\" > .env
```

#### Step 5: Run Application
```bash
streamlit run app.py
```

## Getting Google API Key

### Step-by-Step Guide

1. **Visit Google AI Studio**
   - Go to: https://aistudio.google.com/app/apikey
   - Sign in with your Google account

2. **Create API Key**
   - Click \"Create API Key\" button
   - Choose existing project or create new one
   - Copy the generated API key

3. **Configure Application**
   - Open `.env` file in project directory
   - Replace `your_actual_api_key_here` with your API key
   - Save the file

### API Key Format
```bash
# .env file content
GOOGLE_API_KEY=\"AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\"
```

**Important Notes:**
- Keep your API key secure and private
- Don't share your `.env` file
- The API key should start with `AIza`
- No quotes needed around the key in `.env`

## Platform-Specific Instructions

### Windows

#### Using Command Prompt
```cmd
# Clone repository
git clone https://github.com/yourusername/youtube-video-summarizer.git
cd youtube-video-summarizer

# Create virtual environment
python -m venv venv
venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

#### Using PowerShell
```powershell
# Enable script execution (if needed)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Clone and setup
git clone https://github.com/yourusername/youtube-video-summarizer.git
Set-Location youtube-video-summarizer
python -m venv venv
venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

### macOS

#### Using Homebrew (Recommended)
```bash
# Install Python if needed
brew install python@3.10

# Clone repository
git clone https://github.com/yourusername/youtube-video-summarizer.git
cd youtube-video-summarizer

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

#### Using System Python
```bash
# Ensure Python 3.8+ is installed
python3 --version

# Clone and setup
git clone https://github.com/yourusername/youtube-video-summarizer.git
cd youtube-video-summarizer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

### Linux (Ubuntu/Debian)

#### Install Python and Dependencies
```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip python3-venv git

# Clone repository
git clone https://github.com/yourusername/youtube-video-summarizer.git
cd youtube-video-summarizer

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

#### CentOS/RHEL/Fedora
```bash
# Install Python and Git
sudo dnf install python3 python3-pip git  # Fedora
sudo yum install python3 python3-pip git  # CentOS/RHEL

# Follow same steps as Ubuntu
git clone https://github.com/yourusername/youtube-video-summarizer.git
cd youtube-video-summarizer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Troubleshooting Installation

### Common Issues and Solutions

#### Python Not Found
```bash
# Error: 'python' is not recognized
# Solution: Use python3 instead
python3 --version
python3 -m pip install --upgrade pip
```

#### Permission Errors
```bash
# Linux/Mac: Permission denied
sudo chown -R $(whoami) ~/.local

# Windows: Run as Administrator
# Right-click Command Prompt → \"Run as Administrator\"
```

#### Package Installation Failures
```bash
# Clear pip cache
pip cache purge

# Upgrade pip
python -m pip install --upgrade pip

# Install with no cache
pip install --no-cache-dir -r requirements.txt

# Install individual packages
pip install streamlit
pip install langchain-google-genai
pip install youtube-transcript-api
```

#### Virtual Environment Issues
```bash
# Remove existing venv
rm -rf venv  # Linux/Mac
rmdir /s venv  # Windows

# Create new venv
python -m venv venv

# Activate and reinstall
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate  # Windows
pip install -r requirements.txt
```

#### Streamlit Port Issues
```bash
# Use different port
streamlit run app.py --server.port 8502

# Check for running processes
lsof -i :8501  # Linux/Mac
netstat -ano | findstr :8501  # Windows
```

### Dependency Conflicts

#### Version Conflicts
```bash
# Check installed versions
pip list
pip show streamlit
pip show langchain

# Force reinstall specific versions
pip install --force-reinstall streamlit==1.28.0
pip install --force-reinstall langchain-google-genai==1.0.0
```

#### Clean Installation
```bash
# Remove all packages
pip freeze > packages.txt
pip uninstall -r packages.txt -y

# Fresh install
pip install -r requirements.txt
```

## Verification

### Test Installation
```bash
# Test Python imports
python -c \"import streamlit; print('Streamlit OK')\"
python -c \"import langchain; print('LangChain OK')\"
python -c \"from youtube_transcript_api import YouTubeTranscriptApi; print('YouTube API OK')\"

# Test application imports
python -c \"from app import validate_youtube_url; print('App imports OK')\"

# Test URL validation
python -c \"from app import validate_youtube_url; print(validate_youtube_url('https://youtube.com/watch?v=test'))\"
```

### Performance Check
```bash
# Check Python version
python --version

# Check available memory
free -h  # Linux
Get-ComputerInfo | Select-Object TotalPhysicalMemory, AvailablePhysicalMemory  # Windows PowerShell

# Check disk space
df -h  # Linux/Mac
Get-PSDrive  # Windows PowerShell
```

## Next Steps

After successful installation:

1. **Configure API Key**: Add your Google API key to `.env`
2. **Test Application**: Run with a sample YouTube URL
3. **Read Documentation**: Check [API Reference](api/README.md)
4. **Explore Examples**: See [examples/](examples/) directory
5. **Report Issues**: Use [GitHub Issues](https://github.com/yourusername/youtube-video-summarizer/issues) if needed

## Development Installation

For contributors and developers:

```bash
# Clone with full history
git clone https://github.com/yourusername/youtube-video-summarizer.git
cd youtube-video-summarizer

# Create development environment
python -m venv venv-dev
source venv-dev/bin/activate

# Install with development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available

# Install pre-commit hooks
pre-commit install  # If using pre-commit

# Run tests
pytest tests/  # If tests available

# Start development server
streamlit run app.py --server.runOnSave true
```

For more development information, see [CONTRIBUTING.md](../CONTRIBUTING.md).