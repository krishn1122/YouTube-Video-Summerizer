# Usage Examples

## Basic Usage

### Simple Video Summarization

```python
# Example 1: Basic usage
url = \"https://www.youtube.com/watch?v=dQw4w9WgXcQ\"

# Step 1: Validate URL
from app import validate_youtube_url
if validate_youtube_url(url):
    print(\"✅ Valid YouTube URL\")
else:
    print(\"❌ Invalid URL\")

# Step 2: Extract video ID
from app import extract_video_id
video_id = extract_video_id(url)
print(f\"Video ID: {video_id}\")

# Step 3: Load transcript
from app import load_video_transcript
transcript = load_video_transcript(url)
if transcript:
    print(f\"Transcript loaded: {len(transcript)} characters\")

# Step 4: Generate summary
from app import initialize_llm, summarize_transcript
llm = initialize_llm()
summary = summarize_transcript(llm, transcript)
print(\"Summary:\", summary)
```

## Web Interface Examples

### Test URLs for Different Scenarios

```python
# Educational content
educational_urls = [
    \"https://www.youtube.com/watch?v=3QDYbQIS8cQ\",  # Python tutorial
    \"https://www.youtube.com/watch?v=rfscVS0vtbw\",  # Math explanation
    \"https://www.youtube.com/watch?v=Nt-7WVaC6AQ\"   # Science documentary
]

# Tech talks and presentations
tech_urls = [
    \"https://www.youtube.com/watch?v=8pTEmbeENF4\",  # Google I/O talk
    \"https://www.youtube.com/watch?v=cKzP61Gjf00\",  # TED talk on AI
    \"https://www.youtube.com/watch?v=aircAruvnKk\"   # Neural networks
]

# News and interviews
news_urls = [
    \"https://www.youtube.com/watch?v=example1\",     # News interview
    \"https://www.youtube.com/watch?v=example2\",     # Press conference
    \"https://www.youtube.com/watch?v=example3\"      # Documentary
]
```

### URL Format Examples

```python
# All these formats are supported:
supported_formats = {
    \"standard\": \"https://www.youtube.com/watch?v=dQw4w9WgXcQ\",
    \"with_params\": \"https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=30s\",
    \"short\": \"https://youtu.be/dQw4w9WgXcQ\",
    \"short_with_time\": \"https://youtu.be/dQw4w9WgXcQ?t=30\",
    \"embed\": \"https://www.youtube.com/embed/dQw4w9WgXcQ\",
    \"mobile\": \"https://m.youtube.com/watch?v=dQw4w9WgXcQ\"
}

# Test URL validation
from app import validate_youtube_url
for format_name, url in supported_formats.items():
    is_valid = validate_youtube_url(url)
    print(f\"{format_name}: {'✅' if is_valid else '❌'} {url}\")
```

## Advanced Usage Patterns

### Batch Processing Multiple Videos

```python
import time
from typing import List, Dict
from app import (
    validate_youtube_url, 
    extract_video_id, 
    load_video_transcript, 
    initialize_llm, 
    summarize_transcript
)

def process_video_batch(urls: List[str]) -> Dict[str, str]:
    \"\"\"Process multiple YouTube videos and return summaries.\"\"\"
    
    results = {}
    llm = initialize_llm()  # Initialize once for all videos
    
    for i, url in enumerate(urls, 1):
        print(f\"Processing video {i}/{len(urls)}: {url}\")
        
        # Validate URL
        if not validate_youtube_url(url):
            results[url] = \"Error: Invalid YouTube URL\"
            continue
        
        # Extract video ID
        video_id = extract_video_id(url)
        if not video_id:
            results[url] = \"Error: Could not extract video ID\"
            continue
        
        try:
            # Load transcript
            transcript = load_video_transcript(url)
            if not transcript:
                results[url] = \"Error: Could not load transcript\"
                continue
            
            # Generate summary
            summary = summarize_transcript(llm, transcript)
            if summary:
                results[url] = summary
            else:
                results[url] = \"Error: Could not generate summary\"
        
        except Exception as e:
            results[url] = f\"Error: {str(e)}\"
        
        # Rate limiting - respect API limits
        time.sleep(2)  # Wait 2 seconds between requests
    
    return results

# Example usage
video_urls = [
    \"https://www.youtube.com/watch?v=example1\",
    \"https://www.youtube.com/watch?v=example2\",
    \"https://www.youtube.com/watch?v=example3\"
]

summaries = process_video_batch(video_urls)
for url, summary in summaries.items():
    print(f\"\nURL: {url}\")
    print(f\"Summary: {summary[:200]}...\")  # First 200 characters
```

### Custom Summary Templates

```python
from langchain.prompts import PromptTemplate
from app import initialize_llm

# Custom template for technical content
technical_template = PromptTemplate(
    input_variables=[\"video_transcript\"],
    template=\"\"\"
    Analyze this technical video transcript and provide:
    
    1. **Main Topic**: What technology/concept is being discussed?
    2. **Key Technical Points**: List 5 most important technical details
    3. **Prerequisites**: What background knowledge is needed?
    4. **Practical Applications**: How can this be applied in real projects?
    5. **Further Learning**: What should someone study next?
    
    Transcript: {video_transcript}
    \"\"\"
)

# Custom template for educational content
educational_template = PromptTemplate(
    input_variables=[\"video_transcript\"],
    template=\"\"\"
    Create a study guide from this educational video:
    
    1. **Learning Objectives**: What will students learn?
    2. **Key Concepts**: Main ideas explained (max 5)
    3. **Examples Given**: Concrete examples mentioned
    4. **Practice Opportunities**: Suggested exercises or applications
    5. **Assessment Questions**: 3 questions to test understanding
    
    Transcript: {video_transcript}
    \"\"\"
)

def summarize_with_custom_template(transcript: str, template: PromptTemplate) -> str:
    \"\"\"Generate summary using custom template.\"\"\"
    llm = initialize_llm()
    
    try:
        # Use LCEL syntax
        chain = template | llm
        response = chain.invoke({\"video_transcript\": transcript})
        
        if hasattr(response, 'content'):
            return response.content
        else:
            return str(response)
    except Exception as e:
        return f\"Error generating summary: {str(e)}\"

# Example usage
transcript = \"Your video transcript here...\"
technical_summary = summarize_with_custom_template(transcript, technical_template)
print(\"Technical Summary:\", technical_summary)
```

### Error Handling Examples

```python
from app import (
    validate_youtube_url, 
    load_video_transcript, 
    initialize_llm, 
    summarize_transcript
)
import streamlit as st

def robust_video_processing(url: str) -> Dict[str, any]:
    \"\"\"Process video with comprehensive error handling.\"\"\"
    
    result = {
        \"success\": False,
        \"video_id\": None,
        \"transcript\": None,
        \"summary\": None,
        \"errors\": [],
        \"warnings\": []
    }
    
    # Step 1: URL Validation
    try:
        if not validate_youtube_url(url):
            result[\"errors\"].append(\"Invalid YouTube URL format\")
            return result
    except Exception as e:
        result[\"errors\"].append(f\"URL validation error: {str(e)}\")
        return result
    
    # Step 2: Video ID Extraction
    try:
        from app import extract_video_id
        video_id = extract_video_id(url)
        if not video_id:
            result[\"errors\"].append(\"Could not extract video ID\")
            return result
        result[\"video_id\"] = video_id
    except Exception as e:
        result[\"errors\"].append(f\"Video ID extraction error: {str(e)}\")
        return result
    
    # Step 3: Transcript Loading
    try:
        transcript = load_video_transcript(url)
        if not transcript:
            result[\"errors\"].append(\"No transcript available\")
            result[\"warnings\"].append(\"Try using manual transcript input\")
            return result
        
        if len(transcript) < 100:
            result[\"warnings\"].append(\"Transcript seems very short\")
        
        result[\"transcript\"] = transcript
    except Exception as e:
        result[\"errors\"].append(f\"Transcript loading error: {str(e)}\")
        return result
    
    # Step 4: LLM Initialization
    try:
        llm = initialize_llm()
    except Exception as e:
        result[\"errors\"].append(f\"LLM initialization error: {str(e)}\")
        return result
    
    # Step 5: Summary Generation
    try:
        summary = summarize_transcript(llm, transcript)
        if not summary:
            result[\"errors\"].append(\"Failed to generate summary\")
            return result
        
        result[\"summary\"] = summary
        result[\"success\"] = True
        
    except Exception as e:
        result[\"errors\"].append(f\"Summary generation error: {str(e)}\")
        return result
    
    return result

# Example usage with error handling
def process_video_safely(url: str):
    \"\"\"Process video with user-friendly error reporting.\"\"\"
    
    result = robust_video_processing(url)
    
    if result[\"success\"]:
        print(\"✅ Video processed successfully!\")
        print(f\"Video ID: {result['video_id']}\")
        print(f\"Transcript length: {len(result['transcript'])} characters\")
        print(f\"Summary: {result['summary'][:200]}...\")
        
        if result[\"warnings\"]:
            print(\"⚠️ Warnings:\")
            for warning in result[\"warnings\"]:
                print(f\"  - {warning}\")
    else:
        print(\"❌ Video processing failed!\")
        print(\"Errors:\")
        for error in result[\"errors\"]:
            print(f\"  - {error}\")
        
        if result[\"warnings\"]:
            print(\"Suggestions:\")
            for warning in result[\"warnings\"]:
                print(f\"  - {warning}\")

# Test with various URLs
test_urls = [
    \"https://www.youtube.com/watch?v=valid_video_id\",  # Should work
    \"https://invalid-url.com\",                          # Invalid URL
    \"https://www.youtube.com/watch?v=nonexistent\",      # No transcript
]

for url in test_urls:
    print(f\"\nTesting: {url}\")
    process_video_safely(url)
```

## Integration Examples

### Save Summaries to Files

```python
import os
from datetime import datetime
from app import extract_video_id

def save_summary(url: str, summary: str, output_dir: str = \"summaries\") -> str:
    \"\"\"Save summary to file with organized naming.\"\"\"
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate filename
    video_id = extract_video_id(url)
    timestamp = datetime.now().strftime(\"%Y%m%d_%H%M%S\")
    filename = f\"{video_id}_{timestamp}_summary.txt\"
    filepath = os.path.join(output_dir, filename)
    
    # Save summary
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f\"YouTube Video Summary\n\")
        f.write(f\"=====================\n\n\")
        f.write(f\"URL: {url}\n\")
        f.write(f\"Video ID: {video_id}\n\")
        f.write(f\"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n\")
        f.write(f\"Summary:\n\")
        f.write(f\"--------\n\")
        f.write(summary)
    
    return filepath

# Example usage
url = \"https://www.youtube.com/watch?v=example\"
summary = \"Your generated summary here...\"
file_path = save_summary(url, summary)
print(f\"Summary saved to: {file_path}\")
```

### Export to Different Formats

```python
import json
import csv
from typing import Dict, List

def export_summaries(summaries: Dict[str, str], format: str = \"json\") -> str:
    \"\"\"Export summaries to various formats.\"\"\"
    
    timestamp = datetime.now().strftime(\"%Y%m%d_%H%M%S\")
    
    if format.lower() == \"json\":
        filename = f\"summaries_{timestamp}.json\"
        data = {
            \"export_date\": datetime.now().isoformat(),
            \"total_videos\": len(summaries),
            \"summaries\": [
                {
                    \"url\": url,
                    \"video_id\": extract_video_id(url),
                    \"summary\": summary
                }
                for url, summary in summaries.items()
            ]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    elif format.lower() == \"csv\":
        filename = f\"summaries_{timestamp}.csv\"
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([\"URL\", \"Video_ID\", \"Summary\"])
            
            for url, summary in summaries.items():
                video_id = extract_video_id(url)
                # Clean summary for CSV (remove newlines, quotes)
                clean_summary = summary.replace('\n', ' ').replace('\"', '\"\"')
                writer.writerow([url, video_id, clean_summary])
    
    elif format.lower() == \"markdown\":
        filename = f\"summaries_{timestamp}.md\"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(\"# YouTube Video Summaries\n\n\")
            f.write(f\"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n\")
            
            for i, (url, summary) in enumerate(summaries.items(), 1):
                video_id = extract_video_id(url)
                f.write(f\"## Video {i}: {video_id}\n\n\")
                f.write(f\"**URL:** {url}\n\n\")
                f.write(f\"**Summary:**\n{summary}\n\n\")
                f.write(\"---\n\n\")
    
    return filename

# Example usage
summaries = {
    \"https://www.youtube.com/watch?v=example1\": \"Summary 1...\",
    \"https://www.youtube.com/watch?v=example2\": \"Summary 2...\",
}

json_file = export_summaries(summaries, \"json\")
csv_file = export_summaries(summaries, \"csv\")
md_file = export_summaries(summaries, \"markdown\")

print(f\"Exported to:\")
print(f\"  JSON: {json_file}\")
print(f\"  CSV: {csv_file}\")
print(f\"  Markdown: {md_file}\")
```

## Performance Optimization

### Caching Results

```python
import hashlib
import pickle
import os
from typing import Optional

class SummaryCache:
    \"\"\"Cache summaries to avoid regenerating for same videos.\"\"\"
    
    def __init__(self, cache_dir: str = \"cache\"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_cache_key(self, url: str) -> str:
        \"\"\"Generate cache key from URL.\"\"\"
        video_id = extract_video_id(url)
        return hashlib.md5(video_id.encode()).hexdigest()
    
    def get(self, url: str) -> Optional[str]:
        \"\"\"Get cached summary if available.\"\"\"
        cache_key = self._get_cache_key(url)
        cache_file = os.path.join(self.cache_dir, f\"{cache_key}.pkl\")
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'rb') as f:
                    return pickle.load(f)
            except Exception:
                # Remove corrupted cache file
                os.remove(cache_file)
        
        return None
    
    def set(self, url: str, summary: str) -> None:
        \"\"\"Cache summary for URL.\"\"\"
        cache_key = self._get_cache_key(url)
        cache_file = os.path.join(self.cache_dir, f\"{cache_key}.pkl\")
        
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(summary, f)
        except Exception as e:
            print(f\"Warning: Could not cache summary: {e}\")
    
    def clear(self) -> None:
        \"\"\"Clear all cached summaries.\"\"\"
        for filename in os.listdir(self.cache_dir):
            if filename.endswith('.pkl'):
                os.remove(os.path.join(self.cache_dir, filename))

# Usage with caching
cache = SummaryCache()

def get_summary_with_cache(url: str) -> str:
    \"\"\"Get summary with caching support.\"\"\"
    
    # Check cache first
    cached_summary = cache.get(url)
    if cached_summary:
        print(\"📋 Using cached summary\")
        return cached_summary
    
    # Generate new summary
    print(\"🔄 Generating new summary\")
    transcript = load_video_transcript(url)
    if not transcript:
        return \"Error: Could not load transcript\"
    
    llm = initialize_llm()
    summary = summarize_transcript(llm, transcript)
    
    if summary:
        # Cache the result
        cache.set(url, summary)
        return summary
    else:
        return \"Error: Could not generate summary\"

# Example usage
url = \"https://www.youtube.com/watch?v=example\"
summary1 = get_summary_with_cache(url)  # Will generate
summary2 = get_summary_with_cache(url)  # Will use cache
```

These examples demonstrate various ways to use the YouTube Video Summarizer beyond the basic web interface, including batch processing, custom templates, error handling, and performance optimization.