import streamlit as st
import os
import warnings
import re
from dotenv import load_dotenv

# Suppress warnings
warnings.filterwarnings("ignore")

# Configure Streamlit page
st.set_page_config(
    page_title="YouTube Video Summarizer - Google Gemini",
    page_icon="📹",
    layout="wide"
)

# Load environment variables
load_dotenv(override=True)

def validate_youtube_url(url):
    """Validate if the provided URL is a valid YouTube URL."""
    youtube_patterns = [
        r'^(https?://)?(www\.)?(youtube\.com/watch\?v=)([a-zA-Z0-9_-]{11})',
        r'^(https?://)?(www\.)?(youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'^(https?://)?(www\.)?(youtube\.com/embed/)([a-zA-Z0-9_-]{11})'
    ]
    
    for pattern in youtube_patterns:
        if re.match(pattern, url):
            return True
    return False

def extract_video_id(url):
    """Extract video ID from YouTube URL."""
    patterns = [
        r'(?:v=|/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed/|v/|.+\?v=|watch\?.*v=)([A-Za-z0-9_-]{11})',
        r'(?:youtu\.be/)([A-Za-z0-9_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            video_id = match.group(1)
            if len(video_id) == 11:
                return video_id
    return None

@st.cache_resource
def initialize_llm():
    """Initialize the Google Gemini LLM with caching."""
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key or api_key == "your_actual_api_key_here":
        st.error("⚠️ GOOGLE_API_KEY not configured. Please set it in your .env file.")
        st.info("Get your API key from: https://aistudio.google.com/app/apikey")
        st.stop()
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=api_key,
            temperature=0.0,
            convert_system_message_to_human=True
        )
        return llm
    except ImportError:
        st.error("Missing langchain-google-genai package. Please install: pip install langchain-google-genai")
        st.stop()
    except Exception as e:
        st.error(f"Failed to initialize Gemini LLM: {str(e)}")
        st.stop()

def create_summarizer_template():
    """Create the prompt template for video summarization."""
    try:
        from langchain.prompts import PromptTemplate
        
        return PromptTemplate(
            input_variables=["video_transcript"],
            template="""
            Read through the entire transcript carefully.
            Provide a concise summary of the video's main topic and purpose.
            Extract and list the five most interesting or important points from the transcript.

            -Ensure your summary and key points capture the essence of the video without including unnecessary details.
            -Use clear, engaging language that is accessible to a general audience.
            -If the transcript includes any statistical data, expert opinion, or unique insights,
            prioritize including these in your summary or key points.

            Video transcript: {video_transcript}
            """
        )
    except ImportError:
        st.error("Missing langchain package. Please install: pip install langchain")
        st.stop()

def load_video_transcript(video_url):
    """Load transcript from YouTube video using reliable methods."""
    video_id = extract_video_id(video_url)
    if not video_id:
        st.error("❌ Could not extract video ID from URL.")
        return None
    
    # Method 1: Try youtube-transcript-api
    try:
        with st.spinner("🔄 Loading transcript via YouTube API..."):
            from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
            
            try:
                transcript_data = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
                st.success("✅ English transcript loaded!")
            except NoTranscriptFound:
                try:
                    transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
                    st.success("✅ Transcript loaded (auto-detected language)!")
                except NoTranscriptFound:
                    st.warning("⚠️ No transcripts found via API")
                    transcript_data = None
            except TranscriptsDisabled:
                st.warning("⚠️ Transcripts disabled for this video")
                transcript_data = None
            
            if transcript_data:
                transcript = ' '.join([entry['text'] for entry in transcript_data])
                return transcript
                
    except ImportError:
        st.warning("⚠️ youtube-transcript-api not installed")
    except Exception as e:
        st.warning(f"⚠️ API method failed: {str(e)}")
    
    # Method 2: Try LangChain YoutubeLoader
    try:
        with st.spinner("🔄 Loading transcript via LangChain..."):
            from langchain_community.document_loaders import YoutubeLoader
            
            loader = YoutubeLoader.from_youtube_url(video_url, add_video_info=False)
            data = loader.load()
            
            if data and data[0].page_content:
                st.success("✅ Transcript loaded via LangChain!")
                return data[0].page_content
            else:
                st.warning("⚠️ LangChain returned empty data")
                
    except ImportError:
        st.warning("⚠️ langchain-community not installed")
    except Exception as e:
        st.warning(f"⚠️ LangChain method failed: {str(e)}")
    
    # Method 3: Manual input fallback
    st.error("❌ Automatic transcript loading failed.")
    
    with st.expander("📝 Manual Transcript Input", expanded=True):
        st.markdown("""
        **Manual workaround:**
        1. Go to the YouTube video
        2. Click "Show transcript" below the video
        3. Copy the transcript text
        4. Paste it below and click "Use Manual Transcript"
        """)
        
        manual_transcript = st.text_area(
            "Paste transcript here:",
            height=200,
            placeholder="Paste the video transcript here..."
        )
        
        if st.button("🚀 Use Manual Transcript"):
            if manual_transcript.strip():
                st.success("✅ Manual transcript accepted!")
                return manual_transcript.strip()
            else:
                st.warning("⚠️ Please paste a transcript first.")
    
    return None

def summarize_transcript(llm, transcript):
    """Summarize the video transcript using the LLM."""
    try:
        with st.spinner("🤖 Generating summary..."):
            summarizer_template = create_summarizer_template()
            
            # Try modern LCEL syntax first
            try:
                chain = summarizer_template | llm
                response = chain.invoke({"video_transcript": transcript})
                
                if hasattr(response, 'content'):
                    return response.content
                else:
                    return str(response)
                    
            except Exception:
                # Fallback to traditional LLMChain
                from langchain.chains import LLMChain
                
                chain = LLMChain(llm=llm, prompt=summarizer_template)
                return chain.predict(video_transcript=transcript)
                
    except Exception as e:
        st.error(f"❌ Error generating summary: {str(e)}")
        return None

def main():
    """Main Streamlit application."""
    
    # Header
    st.title("📹 YouTube Video Summarizer (Powered by Google Gemini)")
    st.markdown("---")
    st.markdown("### Transform YouTube videos into concise, insightful summaries powered by AI")
    
    # Sidebar
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        This app uses **Google Gemini 1.5 Flash** to:
        - Extract transcripts from YouTube videos
        - Generate comprehensive summaries
        - Highlight key insights and statistics
        """)
        
        st.header("🔧 Configuration")
        st.markdown("""
        - **Model**: Google Gemini 1.5 Flash
        - **Temperature**: 0.0 (Deterministic)
        - **Provider**: Google AI
        """)
        
        st.header("📝 Instructions")
        st.markdown("""
        1. Paste a YouTube video URL
        2. Click 'Summarize Video'
        3. Wait for processing
        4. Review the summary
        """)
        
        st.header("🔧 Setup")
        with st.expander("Installation Guide"):
            st.code("""
# Install required packages
pip install streamlit
pip install python-dotenv
pip install langchain
pip install langchain-community
pip install langchain-google-genai
pip install youtube-transcript-api

# Set up API key in .env file
GOOGLE_API_KEY="your_api_key_here"
            """)
    
    # Initialize LLM
    llm = initialize_llm()
    
    # Main interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        video_url = st.text_input(
            "🔗 Enter YouTube Video URL:",
            placeholder="https://www.youtube.com/watch?v=example",
            help="Paste any YouTube video URL here"
        )
    
    with col2:
        st.write("")  # Spacing
        st.write("")  # Spacing
        summarize_button = st.button("🚀 Summarize Video", type="primary")
    
    # Process video
    if summarize_button:
        if not video_url:
            st.warning("⚠️ Please enter a YouTube URL first.")
        elif not validate_youtube_url(video_url):
            st.error("❌ Please enter a valid YouTube URL.")
        else:
            # Load transcript
            transcript = load_video_transcript(video_url)
            
            if transcript:
                # Show video preview
                st.markdown("### 📺 Video Preview")
                st.video(video_url)
                
                # Generate summary
                summary = summarize_transcript(llm, transcript)
                
                if summary:
                    st.markdown("---")
                    st.markdown("### 📄 AI-Generated Summary")
                    
                    # Create tabs
                    tab1, tab2 = st.tabs(["📝 Summary", "📊 Transcript"])
                    
                    with tab1:
                        st.markdown(summary)
                        
                        # Download option
                        st.download_button(
                            label="💾 Download Summary",
                            data=summary,
                            file_name=f"youtube_summary_{extract_video_id(video_url)}.txt",
                            mime="text/plain"
                        )
                    
                    with tab2:
                        with st.expander("📜 View Full Transcript", expanded=False):
                            st.text_area(
                                "Full Transcript:",
                                transcript,
                                height=300,
                                disabled=True
                            )
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>Built with ❤️ using Streamlit, LangChain, and Google Gemini</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()