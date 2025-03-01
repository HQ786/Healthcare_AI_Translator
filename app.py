import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import base64
import whisper

# Initialize Whisper model for AI-enhanced transcription
whisper_model = whisper.load_model("base")

# Initialize speech recognizer
recognizer = sr.Recognizer()

# Ensure session state for speech output
if "speech_output" not in st.session_state:
    st.session_state.speech_output = None
if "input_speech_output" not in st.session_state:
    st.session_state.input_speech_output = None

def transcribe_speech():
    """Convert speech input into text using AI-enhanced transcription."""
    with sr.Microphone() as source:
        st.info("Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        # Save audio temporarily for Whisper processing
        audio_path = "temp_audio.wav"
        with open(audio_path, "wb") as f:
            f.write(audio.get_wav_data())
        
        # Use Whisper for AI-enhanced transcription
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
