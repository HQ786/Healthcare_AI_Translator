import streamlit as st
import base64
import whisper
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import wave
import io
import pydub
from pydub import AudioSegment
import streamlit.components.v1 as components

# Initialize Whisper model for AI-enhanced transcription
whisper_model = whisper.load_model("base")

# Initialize speech recognizer
recognizer = sr.Recognizer()

# Ensure session state for speech output
if "speech_output" not in st.session_state:
    st.session_state.speech_output = None
if "input_speech_output" not in st.session_state:
    st.session_state.input_speech_output = None
if "audio_data" not in st.session_state:
    st.session_state.audio_data = None

def transcribe_speech(audio_data):
    """Convert speech input into text using AI-enhanced transcription."""
    try:
        audio = AudioSegment.from_wav(io.BytesIO(audio_data))
        audio_path = "temp_audio.wav"
        audio.export(audio_path, format="wav")
        
        # Use Whisper for AI-enhanced transcription
        result = whisper_model.transcribe(audio_path)
        os.remove(audio_path)
        return result["text"]
    except Exception as e:
        return f"Error: {str(e)}"

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

# HTML/JS to access microphone and record audio
html_code = """
    <script>
        async function startRecording() {
            const stream = await navigator.mediaDevices.getUserMedia({audio: true});
            const mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();
            
            let chunks = [];
            mediaRecorder.ondataavailable = (event) => {
                chunks.push(event.data);
            };
            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(chunks, { 'type' : 'audio/wav' });
                const audioUrl = URL.createObjectURL(audioBlob);
                const reader = new FileReader();
                reader.onloadend = function() {
                    const audioBase64 = reader.result.split(',')[1];
                    window.parent.postMessage(audioBase64, "*");
                };
                reader.readAsDataURL(audioBlob);
            };
            
            setTimeout(() => mediaRecorder.stop(), 5000);  // Stop recording after 5 seconds
        }
    </script>
    
    <button onclick="startRecording()">Start Recording</button>
"""

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
    
    components.html(html_code, height=200)  # Embedded HTML/JS for microphone access

    # Handle the received audio data
    if "audio_data" in st.session_state and st.session_state.audio_data:
        st.session_state.audio_data = None
        with st.spinner('Processing audio...'):
            transcribed_text = transcribe_speech(st.session_state.audio_data)
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
