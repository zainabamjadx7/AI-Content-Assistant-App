import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(page_title="AI Content Assistant", page_icon="📝", layout="centered")

st.title("📝 AI Content Assistant")
st.write("Generate tailored captions, posts, and hashtags instantly using Groq!")

# Sidebar for API Key input
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Groq API Key", type="password", help="Get your free key at console.groq.com")

# Main Input Form
with st.form("content_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        platform = st.selectbox("Platform", ["LinkedIn", "Instagram", "Twitter / X", "Facebook"])
        content_type = st.selectbox("Content Type", ["Educational Post", "Promotional / Pitch", "Storytelling", "Quick Tip", "Announcement"])
        tone = st.selectbox("Tone", ["Professional", "Casual & Friendly", "Bold & Energetic", "Humorous", "Inspirational"])
        
    with col2:
        topic = st.text_input("Topic / Subject", placeholder="e.g., Python tips for beginners")
        audience = st.text_input("Target Audience", placeholder="e.g., Software Engineering Students")
    
    submit_button = st.form_submit_button("Generate Content 🚀")

# Generation Logic
if submit_button:
    if not api_key:
        st.error("Please provide a Groq API Key in the sidebar.")
    elif not topic or not audience:
        st.warning("Please fill in both Topic and Target Audience fields.")
    else:
        try:
            client = Groq(api_key=api_key)
            
            prompt = f"""
            You are an expert social media copywriter.
            Create a {platform} post of type '{content_type}'.
            
            - Topic: {topic}
            - Target Audience: {audience}
            - Tone: {tone}
            
            Provide a complete post structure formatted clearly in Markdown:
            1. An engaging hook.
            2. The main post body tailored to {platform}'s best practices.
            3. A clear Call to Action (CTA).
            4. 5-8 relevant hashtags at the bottom.
            """
            
            with st.spinner("Drafting your post..."):
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                )
                
                output = response.choices[0].message.content
                
                st.success("Generated Content:")
                st.markdown(output)
                
        except Exception as e:
            st.error(f"Error generating content: {e}")
