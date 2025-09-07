# Troubleshooting Guide

## Quick Diagnosis

### 🚨 Emergency Checklist

1. **Is Python installed?** → `python --version`
2. **Is the virtual environment activated?** → Check command prompt prefix
3. **Are dependencies installed?** → `pip list | grep streamlit`
4. **Is the API key configured?** → Check `.env` file
5. **Is the application accessible?** → Try `http://localhost:8501`

---

## Common Issues

### 🔑 API Key Problems

#### Issue: \"GOOGLE_API_KEY not configured\"

**Symptoms:**
- Error message on startup
- App stops at initialization
- Red error banner in Streamlit

**Solutions:**

1. **Check `.env` file exists:**
   ```bash
   # Linux/Mac
   ls -la .env
   
   # Windows
   dir .env
   ```

2. **Verify API key format:**
   ```bash
   # Correct format in .env:
   GOOGLE_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   
   # Common mistakes:
   GOOGLE_API_KEY=\"AIza...\"  # ❌ Remove quotes
   GOOGLE_API_KEY = AIza...  # ❌ Remove spaces
   GOOGLEAPI_KEY=AIza...     # ❌ Wrong variable name
   ```

3. **Get new API key:**
   - Visit: https://aistudio.google.com/app/apikey
   - Sign in with Google account
   - Click \"Create API Key\"
   - Copy and paste into `.env` file

4. **Restart application:**
   ```bash
   # Stop current app (Ctrl+C)
   # Restart
   streamlit run app.py
   ```

#### Issue: \"Invalid API key\" or quota errors

**Solutions:**
1. **Check API key permissions:**
   - Ensure Generative AI API is enabled
   - Verify billing is set up (if required)
   
2. **Check quotas:**
   - Free tier: 15 requests/minute, 1,500/day
   - Wait if quota exceeded
   - Upgrade plan if needed

3. **Test API key:**
   ```python
   import os
   from dotenv import load_dotenv
   
   load_dotenv()
   api_key = os.getenv('GOOGLE_API_KEY')
   print(f\"API Key: {api_key[:10]}...{api_key[-5:]}\")
   ```

---

### 📺 Video Processing Issues

#### Issue: \"No transcripts found\"

**Symptoms:**
- Yellow warning message
- Fallback methods also fail
- Video preview works but no text

**Solutions:**

1. **Check video requirements:**
   ```markdown
   Video must have:
   ✅ Public visibility
   ✅ Captions/subtitles enabled
   ✅ Available in your region
   ✅ Not age-restricted
   ```

2. **Try different videos:**
   ```python
   # Test with known working videos:
   test_urls = [
       \"https://www.youtube.com/watch?v=jNQXAC9IVRw\",  # TED talk
       \"https://www.youtube.com/watch?v=aircAruvnKk\",   # 3Blue1Brown
       \"https://www.youtube.com/watch?v=8pTEmbeENF4\"    # Google I/O
   ]
   ```

3. **Check video manually:**
   - Open video on YouTube
   - Look for \"CC\" button (captions)
   - Click settings → Subtitles/CC
   - Verify captions are available

4. **Use manual input:**
   - Copy transcript from YouTube
   - Use manual input option in app
   - Paste and click \"Use Manual Transcript\"

#### Issue: \"Could not extract video ID\"

**Symptoms:**
- Error with URL processing
- Red error message
- Valid-looking YouTube URL

**Solutions:**

1. **Check URL format:**
   ```python
   # Supported formats:
   ✅ https://www.youtube.com/watch?v=VIDEO_ID
   ✅ https://youtu.be/VIDEO_ID
   ✅ https://www.youtube.com/embed/VIDEO_ID
   ✅ https://m.youtube.com/watch?v=VIDEO_ID
   
   # Unsupported formats:
   ❌ https://youtube.com/playlist?list=...
   ❌ https://youtube.com/channel/...
   ❌ https://youtube.com/user/...
   ```

2. **Clean the URL:**
   ```python
   # Remove extra parameters:
   # From: https://youtube.com/watch?v=ID&list=...&t=30s
   # To:   https://youtube.com/watch?v=ID
   ```

3. **Test URL validation:**
   ```python
   from app import validate_youtube_url, extract_video_id
   
   url = \"your_url_here\"
   print(f\"Valid: {validate_youtube_url(url)}\")
   print(f\"Video ID: {extract_video_id(url)}\")
   ```

---

### 🔧 Installation & Dependencies

#### Issue: \"Module not found\" errors

**Symptoms:**
```python
ModuleNotFoundError: No module named 'streamlit'
ModuleNotFoundError: No module named 'langchain_google_genai'
```

**Solutions:**

1. **Check virtual environment:**
   ```bash
   # Activate virtual environment
   # Linux/Mac:
   source venv/bin/activate
   
   # Windows:
   venv\\Scripts\\activate
   
   # Verify activation (should show (venv) prefix)
   ```

2. **Reinstall dependencies:**
   ```bash
   # Upgrade pip first
   python -m pip install --upgrade pip
   
   # Install requirements
   pip install -r requirements.txt
   
   # Verify installation
   pip list | grep streamlit
   pip list | grep langchain
   ```

3. **Install specific packages:**
   ```bash
   # Individual package installation
   pip install streamlit>=1.28.0
   pip install langchain-google-genai>=1.0.0
   pip install youtube-transcript-api>=0.6.0
   ```

4. **Clear pip cache:**
   ```bash
   pip cache purge
   pip install --no-cache-dir -r requirements.txt
   ```

#### Issue: Package version conflicts

**Symptoms:**
- Dependency resolution errors
- Import errors after installation
- Version compatibility warnings

**Solutions:**

1. **Create fresh environment:**
   ```bash
   # Remove old environment
   rm -rf venv  # Linux/Mac
   rmdir /s venv  # Windows
   
   # Create new environment
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\\Scripts\\activate     # Windows
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Check for conflicting packages:**
   ```bash
   pip check
   pip list --outdated
   ```

3. **Use specific versions:**
   ```bash
   # Force specific versions
   pip install streamlit==1.28.0
   pip install langchain==0.1.0
   pip install langchain-google-genai==1.0.0
   ```

---

### 🌐 Network & Connection Issues

#### Issue: \"Connection timeout\" or network errors

**Symptoms:**
- Slow transcript loading
- Network timeout messages
- Failed API requests

**Solutions:**

1. **Check internet connection:**
   ```bash
   # Test connectivity
   ping google.com
   ping youtube.com
   ```

2. **Try different network:**
   - Switch to mobile hotspot
   - Try different WiFi network
   - Check corporate firewall settings

3. **Configure proxy (if needed):**
   ```bash
   # Set proxy environment variables
   export HTTP_PROXY=http://proxy:port
   export HTTPS_PROXY=http://proxy:port
   ```

4. **Retry with backoff:**
   - App has built-in retry logic
   - Wait a few seconds and try again
   - Check YouTube API status

#### Issue: \"Regional restrictions\" or geo-blocking

**Solutions:**
1. **Try different videos:**
   - Use videos from different regions
   - Test with popular, global content

2. **Use VPN (if allowed):**
   - Connect to different country
   - Retry video processing

---

### 🚀 Performance Issues

#### Issue: Slow processing or timeouts

**Symptoms:**
- Long loading times
- App becomes unresponsive
- Timeout errors

**Solutions:**

1. **Check system resources:**
   ```bash
   # Check memory usage
   free -h  # Linux
   Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 10  # Windows
   
   # Check CPU usage
   top  # Linux
   Get-Counter \"\\Processor(_Total)\\% Processor Time\"  # Windows
   ```

2. **Optimize for performance:**
   ```python
   # Use shorter videos for testing
   # Clear browser cache
   # Restart Streamlit app
   # Close other applications
   ```

3. **Adjust processing:**
   - Try videos under 10 minutes first
   - Process one video at a time
   - Restart app between sessions

---

### 🎨 UI & Interface Issues

#### Issue: \"Address already in use\" or port conflicts

**Symptoms:**
```bash
OSError: [Errno 48] Address already in use
Streamlit server could not start
```

**Solutions:**

1. **Use different port:**
   ```bash
   streamlit run app.py --server.port 8502
   streamlit run app.py --server.port 8503
   ```

2. **Kill existing processes:**
   ```bash
   # Linux/Mac
   lsof -ti:8501 | xargs kill -9
   
   # Windows
   netstat -ano | findstr :8501
   taskkill /PID <PID_NUMBER> /F
   ```

3. **Restart system:**
   - Sometimes simplest solution
   - Clears all port conflicts

#### Issue: Page not loading or blank screen

**Solutions:**

1. **Check browser:**
   - Try different browser
   - Clear browser cache
   - Disable ad blockers
   - Check JavaScript is enabled

2. **Check URL:**
   ```bash
   # Correct URLs:
   http://localhost:8501
   http://127.0.0.1:8501
   
   # Check network tab in browser dev tools
   ```

3. **Restart app:**
   ```bash
   # Stop app (Ctrl+C)
   # Clear cache
   streamlit cache clear
   # Restart
   streamlit run app.py
   ```

---

## Advanced Troubleshooting

### 🔍 Debug Mode

Enable debug information:

```bash
# Run with debug logging
streamlit run app.py --logger.level debug

# Or set environment variable
STREAMLIT_LOG_LEVEL=debug streamlit run app.py
```

### 📝 Log Analysis

Check Streamlit logs:

```bash
# Find log directory
streamlit config show

# Common log locations:
# Linux/Mac: ~/.streamlit/logs/
# Windows: %APPDATA%/streamlit/logs/

# View recent logs
tail -f ~/.streamlit/logs/streamlit.log
```

### 🧪 Component Testing

Test individual components:

```python
# Test script: test_components.py

def test_imports():
    try:
        import streamlit as st
        print(\"✅ Streamlit import OK\")
    except ImportError as e:
        print(f\"❌ Streamlit import failed: {e}\")
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        print(\"✅ LangChain Google import OK\")
    except ImportError as e:
        print(f\"❌ LangChain Google import failed: {e}\")
    
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        print(\"✅ YouTube API import OK\")
    except ImportError as e:
        print(f\"❌ YouTube API import failed: {e}\")

def test_url_validation():
    from app import validate_youtube_url, extract_video_id
    
    test_cases = [
        \"https://www.youtube.com/watch?v=dQw4w9WgXcQ\",
        \"https://youtu.be/dQw4w9WgXcQ\",
        \"invalid-url\"
    ]
    
    for url in test_cases:
        valid = validate_youtube_url(url)
        video_id = extract_video_id(url)
        print(f\"URL: {url}\")
        print(f\"  Valid: {valid}\")
        print(f\"  Video ID: {video_id}\")
        print()

if __name__ == \"__main__\":
    test_imports()
    test_url_validation()
```

Run the test:
```bash
python test_components.py
```

---

## Getting Help

### 📞 Support Channels

1. **GitHub Issues** (Primary):
   - https://github.com/yourusername/youtube-video-summarizer/issues
   - Use issue templates
   - Provide detailed information

2. **Discussions**:
   - https://github.com/yourusername/youtube-video-summarizer/discussions
   - Community Q&A
   - Feature requests

3. **Documentation**:
   - [Installation Guide](installation.md)
   - [API Reference](api/README.md)
   - [Usage Examples](examples/usage-examples.md)

### 📋 When Reporting Issues

Include this information:

```markdown
**Environment:**
- OS: [Windows 10 / macOS 12 / Ubuntu 20.04]
- Python version: [3.9.7]
- Browser: [Chrome 95.0]
- App version: [1.0.0]

**Steps to reproduce:**
1. Start application
2. Enter URL: https://youtube.com/watch?v=...
3. Click \"Summarize Video\"
4. See error

**Expected behavior:**
Should generate summary

**Actual behavior:**
Error message: \"...\"

**Screenshots:**
[Attach error screenshots]

**Logs:**
[Include relevant log output]

**Additional context:**
[Any other relevant information]
```

### 🔄 Version Information

Get version information:

```python
# version_info.py
import sys
import streamlit as st
import langchain
import platform

print(\"System Information:\")
print(f\"Platform: {platform.platform()}\")
print(f\"Python: {sys.version}\")
print(f\"Streamlit: {st.__version__}\")
print(f\"LangChain: {langchain.__version__}\")

try:
    import youtube_transcript_api
    print(f\"YouTube Transcript API: {youtube_transcript_api.__version__}\")
except:
    print(\"YouTube Transcript API: Unknown version\")

try:
    from langchain_google_genai import __version__
    print(f\"LangChain Google GenAI: {__version__}\")
except:
    print(\"LangChain Google GenAI: Unknown version\")
```

---

**Remember**: Most issues can be resolved by following the basic checklist at the top of this guide. When in doubt, try the simplest solution first! 🚀