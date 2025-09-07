# API Reference

## Core Functions

### `validate_youtube_url(url: str) -> bool`

Validates if the provided URL is a valid YouTube URL.

**Parameters:**
- `url` (str): The URL to validate

**Returns:**
- `bool`: True if URL is valid YouTube URL, False otherwise

**Supported URL Formats:**
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`

**Example:**
```python
from app import validate_youtube_url

url = \"https://www.youtube.com/watch?v=dQw4w9WgXcQ\"
if validate_youtube_url(url):
    print(\"Valid YouTube URL\")
```

### `extract_video_id(url: str) -> Optional[str]`

Extracts the video ID from a YouTube URL.

**Parameters:**
- `url` (str): YouTube URL

**Returns:**
- `str` or `None`: 11-character video ID if found, None otherwise

**Example:**
```python
from app import extract_video_id

url = \"https://www.youtube.com/watch?v=dQw4w9WgXcQ\"
video_id = extract_video_id(url)
print(f\"Video ID: {video_id}\")  # Output: dQw4w9WgXcQ
```

### `initialize_llm() -> ChatGoogleGenerativeAI`

Initializes the Google Gemini LLM with caching.

**Returns:**
- `ChatGoogleGenerativeAI`: Configured Gemini model instance

**Configuration:**
- Model: `gemini-1.5-flash`
- Temperature: `0.0` (deterministic)
- API Key: Read from `GOOGLE_API_KEY` environment variable

**Example:**
```python
from app import initialize_llm

llm = initialize_llm()
# LLM is ready for use
```

### `load_video_transcript(video_url: str) -> Optional[str]`

Loads transcript from YouTube video using multiple fallback methods.

**Parameters:**
- `video_url` (str): Full YouTube video URL

**Returns:**
- `str` or `None`: Video transcript if successful, None if all methods fail

**Extraction Methods (in order):**
1. **YouTube Transcript API** - Direct API access
2. **LangChain YoutubeLoader** - Alternative extraction method
3. **Manual Input** - User-provided transcript

**Example:**
```python
from app import load_video_transcript

url = \"https://www.youtube.com/watch?v=dQw4w9WgXcQ\"
transcript = load_video_transcript(url)
if transcript:
    print(f\"Transcript length: {len(transcript)} characters\")
```

### `summarize_transcript(llm, transcript: str) -> Optional[str]`

Generates AI summary of video transcript using Google Gemini.

**Parameters:**
- `llm`: Initialized LLM instance
- `transcript` (str): Video transcript text

**Returns:**
- `str` or `None`: Generated summary if successful, None on error

**Summary Features:**
- Concise main topic summary
- Five key points extraction
- Accessible language for general audience
- Emphasis on statistics and expert opinions

**Example:**
```python
from app import initialize_llm, summarize_transcript

llm = initialize_llm()
transcript = \"Your video transcript here...\"
summary = summarize_transcript(llm, transcript)
print(summary)
```

## Streamlit Interface

### Main Application

The main Streamlit application (`main()`) provides:

- **URL Input**: Text input for YouTube URLs
- **Video Preview**: Embedded YouTube player
- **Processing Status**: Real-time progress indicators
- **Results Display**: Tabbed interface for summary and transcript
- **Download**: Save summaries as text files

### UI Components

#### Sidebar
- About section with feature overview
- Configuration details
- Step-by-step instructions
- Installation guide

#### Main Interface
- Two-column layout for input and action button
- Video preview section
- Tabbed results (Summary / Transcript)
- Download functionality

## Error Handling

### Common Error Types

1. **API Key Errors**
   ```python
   # Missing or invalid API key
   if not api_key or api_key == \"your_actual_api_key_here\":
       st.error(\"⚠️ GOOGLE_API_KEY not configured\")
   ```

2. **Import Errors**
   ```python
   try:
       from langchain_google_genai import ChatGoogleGenerativeAI
   except ImportError:
       st.error(\"Missing langchain-google-genai package\")
   ```

3. **Transcript Extraction Errors**
   ```python
   try:
       transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
   except NoTranscriptFound:
       st.warning(\"⚠️ No transcripts found via API\")
   ```

### Error Recovery

- **Progressive Fallback**: Multiple extraction methods
- **User Guidance**: Clear error messages with solutions
- **Manual Override**: Always available manual input option
- **Graceful Degradation**: Application continues despite individual failures

## Configuration

### Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `GOOGLE_API_KEY` | Yes | Google Gemini API key | `AIza...` |

### Model Settings

```python
CHATGOOGLEGENERATIVEAI_CONFIG = {
    \"model\": \"gemini-1.5-flash\",
    \"temperature\": 0.0,
    \"convert_system_message_to_human\": True
}
```

### Streamlit Configuration

```python
STREAMLIT_CONFIG = {
    \"page_title\": \"YouTube Video Summarizer - Google Gemini\",
    \"page_icon\": \"📹\",
    \"layout\": \"wide\"
}
```

## Rate Limits & Quotas

### Google Gemini Free Tier

- **Requests per minute**: 15
- **Requests per day**: 1,500
- **Tokens per month**: 1,000,000

### YouTube API Considerations

- **No official rate limits** for transcript API
- **Regional restrictions** may apply
- **Video availability** varies by region

## Best Practices

### Performance

1. **Use caching**: `@st.cache_resource` for LLM initialization
2. **Optimize requests**: Batch multiple operations when possible
3. **Handle timeouts**: Implement retry logic for network operations

### Security

1. **Secure API keys**: Use environment variables, never hardcode
2. **Input validation**: Always validate URLs before processing
3. **Error handling**: Don't expose internal errors to users

### User Experience

1. **Progress indicators**: Show processing status
2. **Clear messaging**: Provide helpful error messages
3. **Fallback options**: Always provide manual alternatives