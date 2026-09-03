import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(
    page_title="AI Content Assistant", 
    page_icon="✨", 
    layout="wide"
)

# Custom CSS for Modern UI
st.markdown("""
    <style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        height: 3em;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.markdown("<div class='main-title'>✨ AI Content Assistant</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Generate tailored captions, posts, and hashtags instantly!</div>", unsafe_allow_html=True)

# Fetch API Key from Streamlit Secrets
api_key = st.secrets.get("GROQ_API_KEY")

# Input Section inside a styled container
st.subheader("⚙️ Content Parameters")

with st.form("content_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        platform = st.selectbox("Platform", ["LinkedIn", "Instagram", "Twitter / X", "Facebook", "TikTok", "YouTube Shorts"])
        content_type = st.selectbox("Content Type", ["Educational Post", "Promotional / Pitch", "Storytelling", "Quick Tip", "Announcement"])
        
    with col2:
        tone = st.selectbox("Tone", ["Professional", "Casual & Friendly", "Bold & Energetic", "Humorous", "Inspirational"])
        language = st.selectbox("Language", ["English", "Roman Urdu", "Urdu"])

    with col3:
        length = st.select_slider("Post Length", options=["Short (~100 words)", "Medium (~250 words)", "Detailed (~400 words)"])
        topic = st.text_input("Topic / Subject", placeholder="e.g., Python tips for beginners")
    
    audience = st.text_input("Target Audience", placeholder="e.g., Software Engineering Students")
    
    submit_button = st.form_submit_button("🚀 Generate Content")

# Generation Logic
if submit_button:
    if not api_key:
        st.error("⚠️ GROQ_API_KEY missing in Streamlit Secrets!")
    elif not topic or not audience:
        st.warning("⚠️ Topic aur Target Audience fill karna zaroori hai.")
    else:
        try:
            client = Groq(api_key=api_key)
            
            prompt = f"""
            You are an expert social media copywriter.
            Create a {platform} post of type '{content_type}'.
            
            - Topic: {topic}
            - Target Audience: {audience}
            - Tone: {tone}
            - Language: {language}
            - Length: {length}
            
            Provide a complete post structure formatted clearly in Markdown:
            1. An engaging hook.
            2. The main post body tailored to {platform}'s best practices.
            3. A clear Call to Action (CTA).
            4. 5-8 relevant hashtags at the bottom.
            """
            
            with st.spinner("✨ Writing your content..."):
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                )
                
                output = response.choices[0].message.content

                st.markdown("---")
                st.subheader("🎯 Generated Output")
                
                # Interactive Tabs for Output
                tab1, tab2 = st.tabs(["📝 Preview Post", "📄 Raw Text & Export"])
                
                with tab1:
                    st.markdown(output)
                
                with tab2:
                    st.text_area("Copy Raw Output:", output, height=250)
                    st.download_button(
                        label="📥 Download Post (.txt)",
                        data=output,
                        file_name=f"{platform}_post.txt",
                        mime="text/plain"
                    )
                
        except Exception as e:
            st.error(f"Error: {e}")
