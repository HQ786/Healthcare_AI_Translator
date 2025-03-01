import streamlit as st
import sounddevice as sd
import numpy as np
import torch
import whisper
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import base64
import scipy.io.wavfile as wav

# Initialize Whisper model for AI-enhanced transcription
whisper_model = whisper.load_model("base")

# Ensure session state for speech output
if "speech_output" not in st.session_state:
    st.session_state.speech_output = None
if "input_speech_output" not in st.session_state:
    st.session_state.input_speech_output = None

def record_audio(duration=5, samplerate=44100):
    """Record audio from microphone using sounddevice."""
    st.info("Recording... Speak now.")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.int16)
    sd.wait()
    return audio.flatten(), samplerate

def transcribe_speech():
    """Convert speech input into text using AI-enhanced transcription."""
    audio, samplerate = record_audio()
    
    try:
        audio_path = "temp_audio.wav"
        wav.write(audio_path, samplerate, audio)
        
        result = whisper_model.transcribe(audio_path)
        os.remove(audio_path)
        return result["text"], audio
    except Exception as e:
        return f"Error: {str(e)}", None

def translate_text(text, target_language):
    """Translate text using Google Translator."""
    try:
        return GoogleTranslator(source='auto', target=target_language).translate(text)
    except Exception as e:
        return f"Error: {str(e)}"

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

def main():
    st.set_page_config(page_title="AI Voice Translator", page_icon="🎙️", layout="wide")
    st.title("🎙️ AI Voice Translator")
    
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
    
    if st.button("Start Speaking", key="start_speaking"):
        with st.spinner('Listening...'):
            transcribed_text, input_audio = transcribe_speech()
            translated_text = translate_text(transcribed_text, target_language_code)
            st.session_state.speech_output = text_to_speech(translated_text, target_language_code)
            st.session_state.input_speech_output = text_to_speech(transcribed_text, input_language_code)
            
            st.session_state.transcribed_text = transcribed_text
            st.session_state.translated_text = translated_text
    
    st.subheader("Results")
    col1, col2 = st.columns(2)
    with col1:
        st.text_area("Original Transcription:", value=st.session_state.get("transcribed_text", ""), height=100, disabled=True)
        if st.session_state.input_speech_output:
            if st.button("🔊 Speak", key="speak_original"):
                st.markdown(f'<audio controls><source src="{st.session_state.input_speech_output}" type="audio/mp3"></audio>', unsafe_allow_html=True)
    
    with col2:
        st.text_area("Translated Text:", value=st.session_state.get("translated_text", ""), height=100, disabled=True)
        if st.session_state.speech_output:
            if st.button("🔊 Speak", key="speak_translated"):
                st.markdown(f'<audio controls><source src="{st.session_state.speech_output}" type="audio/mp3"></audio>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
