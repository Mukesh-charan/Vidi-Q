import pyttsx3
from pathlib import Path
from config import AUDIO_FILES_DIR, TTS_CONFIG

class AudioGenerator:
    def __init__(self):
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', TTS_CONFIG["rate"])
            self.engine.setProperty('volume', TTS_CONFIG["volume"])
            
            # Try to set a friendly voice for students
            voices = self.engine.getProperty('voices')
            if voices:
                # Prefer a clear, friendly voice for educational content
                for voice in voices:
                    if "david" in voice.name.lower() or "zira" in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        break
        except Exception as e:
            raise Exception(f"Failed to initialize TTS engine: {str(e)}")
    
    def generate_audio(self, transcript, filename="student_explanation"):
        try:
            # On Windows, pyttsx3 saves WAV reliably; MoviePy can ingest WAV
            audio_filename = f"{filename}.wav"
            audio_path = AUDIO_FILES_DIR / audio_filename
            
            # Save audio to file
            self.engine.save_to_file(transcript, str(audio_path))
            self.engine.runAndWait()
            
            return audio_path
            
        except Exception as e:
            raise Exception(f"Failed to generate audio: {str(e)}")
        
        finally:
            self.engine.stop()


