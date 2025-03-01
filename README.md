# Nao Medical AI Voice Translator

An interactive **AI Voice Translator** web application that leverages **AI transcription (Whisper)**, **Google Translate**, and **Text-to-Speech (gTTS)** to provide real-time translations with voice support. Users can speak in one language, and the app will transcribe, translate, and output the translated text in the target language, along with an audio response.

## Features
- **AI-driven transcription** using Whisper for accurate speech-to-text conversion.
- **Real-time translation** using **Google Translator** for various languages.
- **Text-to-Speech** for both the original and translated text using **gTTS** (Google Text-to-Speech).
- **Multi-language support** including English, Spanish, French, German, Italian, Portuguese, Hindi, Chinese, Japanese, Arabic, and Russian.
- **Simple interface** using **Streamlit** for ease of use and fast deployment.

## Installation

To run this app locally, you'll need to install a few dependencies.

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/nao-medical-ai-voice-translator.git
    cd nao-medical-ai-voice-translator
    ```

2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the Streamlit app:

    ```bash
    streamlit run app.py
    ```

4. The app will open in your default web browser.

## Usage

- **Select Input Language**: Choose the language you will speak into the microphone.
- **Select Target Language**: Choose the language you want the translation in.
- **Start Speaking**: Press the "Start Speaking" button, then speak into the microphone. The app will transcribe your speech, translate it, and provide both the transcribed text and the translation in voice format.
- **Audio Controls**: You can listen to both the original transcription and the translated text by clicking the speaker icons next to each text box.

## Supported Languages

- **English** (en)
- **Spanish** (es)
- **French** (fr)
- **German** (de)
- **Italian** (it)
- **Portuguese** (pt)
- **Hindi** (hi)
- **Chinese** (zh)
- **Japanese** (ja)
- **Arabic** (ar)
- **Russian** (ru)

## Technologies Used

- **Streamlit**: Framework for building the app's user interface.
- **Whisper**: OpenAI’s speech-to-text model for transcription.
- **Google Translator**: For translation between various languages.
- **gTTS (Google Text-to-Speech)**: For converting text to speech.
- **Python**: The main programming language.

## Contributing

Feel free to fork the repository and submit pull requests if you have any improvements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- OpenAI’s **Whisper** for advanced speech-to-text transcription.
- **Google Translator** for seamless translation.
- **gTTS** for converting text to speech.
