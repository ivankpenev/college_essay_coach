import os
import assemblyai as aai
from dotenv import load_dotenv
import certifi

# Set the SSL certificate file to the one provided by certifi
os.environ['SSL_CERT_FILE'] = certifi.where()

load_dotenv()

aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

class RealtimeTranscriber:
    def __init__(self, on_final_transcript):
        self.on_final_transcript = on_final_transcript
        self.transcriber = None

    def on_data(self, transcript: aai.RealtimeTranscript):
        if not transcript.text:
            return

        if isinstance(transcript, aai.RealtimeFinalTranscript):
            self.on_final_transcript(transcript.text)
        else:
            print(transcript.text, end="\r")

    def on_error(self, error: aai.RealtimeError):
        print("An error occured:", error)

    def on_open(self, session_opened: aai.RealtimeSessionOpened):
        print("Session ID:", session_opened.session_id)

    def on_close(self):
        print("Closing Session")

    def start(self):
        self.transcriber = aai.RealtimeTranscriber(
            on_data=self.on_data,
            on_error=self.on_error,
            sample_rate=44_100,
            on_open=self.on_open,
            on_close=self.on_close,
        )

        self.transcriber.connect()
        
        print("Listening... (press Ctrl+C to stop)")
        microphone_stream = aai.extras.MicrophoneStream()
        self.transcriber.stream(microphone_stream)

    def stop(self):
        if self.transcriber:
            self.transcriber.close()
            self.transcriber = None

if __name__ == '__main__':
    def handle_final_transcript(text):
        print(f"\nFinal Transcript: {text}")

    transcriber_instance = RealtimeTranscriber(on_final_transcript=handle_final_transcript)
    try:
        transcriber_instance.start()
    except KeyboardInterrupt:
        transcriber_instance.stop()
        print("\nTranscription stopped.") 