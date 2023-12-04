from record import record_audio
from transcribe import transcribe_audio
from cloud import cloud_function, summary_length_options
from send_email import send_email
import os

def main():
    # Record audio and get filename
    min, max = summary_length_options()
    audio_filename = record_audio()

    # Extract timestamp from audio filename
    audiotext = audio_filename.split("_audio.wav")[0]
    timestamp = audiotext.split("/")[2]
    # Construct filenames for transcription and summary
    transcription_filename = f"./transcribes/{timestamp}_transcription.txt"
    summary_filename = f"./summaries/{timestamp}_summary.txt"

    # Transcribe audio
    transcribe_audio(audio_filename, transcription_filename)

    # Summarize text
    url = os.environ.get("GCP_URL") #Enter your GCP Cloud Function (Summariser) URL here
    cloud_function(url, transcription_filename, summary_filename, min, max)

    # Send summary to  Email
    send_email(summary_filename)
if __name__ == "__main__":
    main()

