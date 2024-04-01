import streamlit as st
import speech_recognition as sr
import os
import tempfile
from pydub import AudioSegment

# Function to convert audio file to WAV format
def convert_to_wav(uploaded_file):
    # Save the uploaded file to a temporary directory
    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(temp_file_path, 'wb') as temp_file:
        temp_file.write(uploaded_file.read())

    # Check file extension
    _, file_extension = os.path.splitext(uploaded_file.name)
    file_extension = file_extension.lower()

    # Load audio file
    audio = AudioSegment.from_file(temp_file_path, format=file_extension[1:])
    
    # Convert to WAV format
    wav_file = os.path.join(temp_dir, os.path.splitext(uploaded_file.name)[0] + ".wav")
    audio.export(wav_file, format="wav")
    
    return wav_file

# Function to transcribe audio file
def transcribe_audio(uploaded_file):
    wav_file = convert_to_wav(uploaded_file)
    
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(wav_file)
    
    with audio_file as source:
        audio_data = recognizer.record(source)
    
    try:
        transcript = recognizer.recognize_google(audio_data)
        return transcript
    except sr.UnknownValueError:
        return "Unable to transcribe audio"
    except sr.RequestError as e:
        return f"Error: {str(e)}"

def main():
    st.title("Audio Transcription App")
    st.write("Upload an audio file (MP3 or WAV) for transcription:")
    
    uploaded_file = st.file_uploader("Choose an audio file...", type=["mp3", "wav"])
    
    if uploaded_file is not None:
        st.write("Transcription:")
        transcript = transcribe_audio(uploaded_file)
        st.write(transcript)

if __name__ == "__main__":
    main()
