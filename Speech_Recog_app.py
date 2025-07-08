import streamlit as st
import speech_recognition as sr
import threading
import time
import platform
from streamlit.runtime.scriptrunner import add_script_run_ctx
import os

# Beep sound (Windows only)
if platform.system() == "Windows":
    import winsound

# App title
st.title("🗣️ Enhanced Speech Recognition App")

# Session state initialization
if 'paused' not in st.session_state:
    st.session_state.paused = False
if 'running' not in st.session_state:
    st.session_state.running = False
if 'transcript' not in st.session_state:
    st.session_state.transcript = ""

# Select speech recognition API
api_choice = st.selectbox(
    "🔧 Choose Speech Recognition API:",
    ["Google", "Sphinx"]
)

# Language selection
language = st.selectbox(
    "🌐 Select Language:",
    ["en-US", "fr-FR", "es-ES", "de-DE", "ha-NG"]
)

st.markdown("🟡 Please wait for the listening prompt and beep before speaking to ensure your full statement is captured.")

# Function to transcribe speech
def transcribe_speech(api, lang):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        st.info("🎤 Listening will start in 2 seconds. Please get ready...")
        time.sleep(2)

        # Beep sound (Windows only)
        if platform.system() == "Windows":
            winsound.Beep(1000, 400)

        st.info("🎙️ Now listening... Speak now.")

        while st.session_state.running:
            if st.session_state.paused:
                time.sleep(0.5)
                continue

            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=30)

                if api == "Google":
                    text = recognizer.recognize_google(audio, language=lang)
                elif api == "Sphinx":
                    text = recognizer.recognize_sphinx(audio, language=lang)
                else:
                    text = "[Unsupported API]"

                st.session_state.transcript += text + "\n"
                st.success(f"📝 Recognized: {text}")

            except sr.WaitTimeoutError:
                st.warning("⏳ Listening timed out. Try speaking again.")
            except sr.UnknownValueError:
                st.warning("🤷 Speech was unclear. Could not recognize.")
            except sr.RequestError as e:
                st.error(f"❌ Could not request results: {e}")
            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")

            time.sleep(0.5)

# Start button
if st.button("▶️ Start Recording"):
    if not st.session_state.running:
        st.session_state.running = True
        st.session_state.paused = False
        t = threading.Thread(target=transcribe_speech, args=(api_choice, language), daemon=True)
        add_script_run_ctx(t)
        t.start()


# Pause/Resume
col1, col2 = st.columns(2)
with col1:
    if st.button("⏸️ Pause"):
        st.session_state.paused = True
with col2:
    if st.button("⏯️ Resume"):
        st.session_state.paused = False

# Stop and Save
if st.button("⏹️ Stop Recording"):
    st.session_state.running = False
    st.session_state.paused = False
    st.success("✅ Recording Stopped.")

# Display transcript
st.markdown("### 📝 Transcript:")
st.text_area("", value=st.session_state.transcript, height=200)

# Save transcript
if st.button("💾 Save Transcript"):
    filename = "transcription.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(st.session_state.transcript)
    with open(filename, "rb") as f:
        st.download_button("📥 Download Transcript", f, file_name=filename)
