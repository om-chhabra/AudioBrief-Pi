import sounddevice as sd
import wavio
import datetime

def record_audio(duration=59, sample_rate=44100, channels=1):
    current_datetime = datetime.datetime.now()
    output_filename = current_datetime.strftime("./records/%d-%m-%Y_%H-%M_audio.wav")
    
    print(f"Recording audio for {duration} seconds...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels)
    sd.wait()
    wavio.write(output_filename, audio_data, sample_rate, sampwidth=2)
    print(f"Audio saved to {output_filename}")

    return output_filename

if __name__ == "__main__":
    record_audio()
