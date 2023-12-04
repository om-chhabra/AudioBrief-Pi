import speech_recognition as sr

def transcribe_audio(audio_file, output_file):
    recognizer = sr.Recognizer()
    
    try:
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)

            # Google Cloud Speech to Text API (Advanced)- Requires google-cloud-speech & GCP crediential JSON
            #credentials_json = "Add Credentials JSON PATH Here..."
            #text = recognizer.recognize_google_cloud(audio_data, credentials_json=credentials_json, language="en-IN")
            
            #Google Speech to Text API (Regular)
            text = recognizer.recognize_google(audio_data, language="en-IN")
            
            with open(output_file, 'w') as file:
                file.write(text)
            
            print(f"Transcription saved to {output_file}")
            return output_file

    except sr.UnknownValueError:
        print("Google Web Speech API could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Web Speech API; {e}")
    except FileNotFoundError:
        print(f"Audio file '{audio_file}' not found.")

if __name__ == "__main__":
    # Example usage
    audio_file = "./records/26-11-2023_17-01_audio.wav"  # Replace with your audio file path
    output_file = "./transcribes/transcription.txt"
    transcribe_audio(audio_file, output_file)
