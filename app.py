# app.py
import streamlit as st
import os
from datetime import datetime
import uuid

st.set_page_config(page_title="Bolo India: Story & Voice Archive", layout="wide")
st.title("📜 Bolo India: Regional Story & Voice Archive")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.sidebar.header("🌍 Metadata")
language = st.sidebar.selectbox("Language", ["Hindi", "Telugu", "Tamil", "Kannada", "Marathi", "Bengali", "Other"])
region = st.sidebar.text_input("Region / Village / City")
category = st.sidebar.selectbox("Category", ["Folktale", "Proverb", "Story", "Song", "Other"])

st.subheader("🎤 Upload Your Voice or Story")
uploaded_audio = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a"])
text_story = st.text_area("Or type your story/proverb here", height=200)

if st.button("Submit"):
    if not uploaded_audio and not text_story:
        st.warning("Please upload a voice note or enter a text story.")
    else:
        uid = str(uuid.uuid4())[:8]
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        if uploaded_audio:
            audio_path = os.path.join(UPLOAD_DIR, f"{uid}_{uploaded_audio.name}")
            with open(audio_path, "wb") as f:
                f.write(uploaded_audio.read())

        meta = {
            "id": uid,
            "timestamp": timestamp,
            "language": language,
            "region": region,
            "category": category,
            "text": text_story
        }
        meta_path = os.path.join(UPLOAD_DIR, f"{uid}_meta.txt")
        with open(meta_path, "w", encoding="utf-8") as f:
            for key, value in meta.items():
                f.write(f"{key}: {value}\n")

        st.success("✅ Submission received! Thank you for contributing.")

st.subheader("📚 Recent Contributions")
entries = [f for f in os.listdir(UPLOAD_DIR) if f.endswith("_meta.txt")]
for entry in sorted(entries, reverse=True)[:5]:
    with open(os.path.join(UPLOAD_DIR, entry), "r", encoding="utf-8") as f:
        st.text(f.read())
