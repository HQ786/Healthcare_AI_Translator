import streamlit as st
import os
import base64
from deep_translator import GoogleTranslator
from gtts import gTTS
import whisper
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import numpy as np

# Initialize Whisper model for AI-enhanced transcription
whisper_model = whisper.load_model("base")

# Initialize speech recognizer (but now using WebRTC for capturing audio)
recognizer = None  # Not needed, as we're using WebRTC to capture audio

# Ensure session state for speech output
if "speech_output" not in st.session_state:
    st.session_state.speech_output = None
if "input_speech_output" not in st.session_state:
    st.session_state.input_speech_output = None

# Define a class for handling audio from WebRTC
class AudioTransformer:
    def __init__(self):
        self.audio_data = None

    def recv(self, frame):
        # Process the incoming audio frame
        self.audio_data = frame
        return frame

# Factory to create the AudioTransformer
class AudioTransformerFactory:
    def __call__(self):
        return AudioTransformer()

# Function to transcribe speech using Whisper
def transcribe_speech(audio_data):
    """Convert audio data into text using AI-enhanced transcription."""
    try:
        # Temporarily save the audio data for Whisper processing
        audio_path = "temp_audio.wav"
        with open(audio_path, "wb") as f:
            f.write(audio_data)
        
        # Use Whisper for AI-enhanced transcription
        result = whisper_model.transcribe(audio_path)
        os.remove(audio_path)
        return result["text"]
    except Exception as e:
        return f"Error: {str(e)}"

# Function to translate text using Google Translator
def translate_text(text, target_language):
    """Translate text using Google Translator."""
    try:
        return GoogleTranslator(source='auto', target=target_language).translate(text)
    except Exception as e:
        return f"Error: {str(e)}"

# Function to convert text to speech
def text_to_speech(text, language):
    """Convert text to speech and return base64 encoded audio."""
    try:
        tts = gTTS(text=text, lang=language, slow=False)
        audio_path = "temp_audio.mp3"
        tts.save(audio_path)
        
        with open(audio_path, "rb") as audio_file:
            audio_base64 = base64.b64encode(audio_file.read()).decode()
        os.remove(audio_path)
        return f"data:audio/mp3;base64,{audio_base64}"
    except Exception as e:
        st.error(f"Error generating speech: {str(e)}")
        return None

# Main function to run the Streamlit app
def main():
    st.set_page_config(page_title="AI Voice Translator", page_icon="🎙️", layout="wide")
    st.title("🎙️ Nao Medical AI Voice Translator")

    language_mapping = {
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'it': 'Italian',
        'pt': 'Portuguese',
        'hi': 'Hindi',
        'zh': 'Chinese',
        'ja': 'Japanese',
        'ar': 'Arabic',
        'ru': 'Russian'
    }
    
    input_language = st.sidebar.selectbox("Select Input Language", list(language_mapping.values()))
    target_language = st.sidebar.selectbox("Select Target Language", list(language_mapping.values())[1:])
    
    input_language_code = list(language_mapping.keys())[list(language_mapping.values()).index(input_language)]
    target_language_code = list(language_mapping.keys())[list(language_mapping.values()).index(target_language)]

    # Set up WebRTC stream for audio capture
    rtc_configuration = RTCConfiguration({
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    })
    
    # Start WebRTC stream for capturing audio
    webrtc_streamer(
        key="audio-input",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=rtc_configuration,
        audio_transformer_factory=AudioTransformerFactory,
        video_transformer_factory=None  # Only need audio in this case
    )
    
    # Process audio data if available
    if "audio_data" in st.session_state:
        audio_data = st.session_state.audio_data
        if audio_data:
            with st.spinner("Processing audio..."):
                transcribed_text = transcribe_speech(audio_data)
                translated_text = translate_text(transcribed_text, target_language_code)
                st.session_state.speech_output = text_to_speech(translated_text, target_language_code)
                st.session_state.input_speech_output = text_to_speech(transcribed_text, input_language_code)
                
                st.session_state.transcribed_text = transcribed_text
                st.session_state.translated_text = translated_text
    
    # Show the results
    st.subheader("Results")
    col1, col2 = st.columns(2)
    with col1:
        st.text_area("Original Transcription:", value=st.session_state.get("transcribed_text", ""), height=100, disabled=True)
        if st.session_state.input_speech_output:
            if st.button("🔊 Speak Original", key="speak_original"):
                st.markdown(f'<audio controls><source src="{st.session_state.input_speech_output}" type="audio/mp3"></audio>', unsafe_allow_html=True)
    
    with col2:
        st.text_area("Translated Text:", value=st.session_state.get("translated_text", ""), height=100, disabled=True)
        if st.session_state.speech_output:
            if st.button("🔊 Speak Translated", key="speak_translated"):
                st.markdown(f'<audio controls><source src="{st.session_state.speech_output}" type="audio/mp3"></audio>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

