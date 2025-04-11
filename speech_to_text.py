import speech_recognition as sr
import threading
import queue
import time

class SpeechToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.text_queue = queue.Queue()
        self.is_recording = False
        self.thread = None
        self.recording_timeout = 5  # Maximum recording time in seconds

        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)

    def _record_audio(self):
        """Record audio with timeout"""
        try:
            with self.microphone as source:
                print("Recording...")
                start_time = time.time()
                
                # Listen with a shorter timeout and phrase time limit
                audio = self.recognizer.listen(
                    source, 
                    timeout=1,
                    phrase_time_limit=self.recording_timeout
                )
                
                try:
                    text = self.recognizer.recognize_google(audio)
                    print(f"Recognized: {text}")
                    self.text_queue.put(text)
                except sr.UnknownValueError:
                    print("Could not understand audio")
                except sr.RequestError as e:
                    print(f"Could not request results; {e}")
                
                # Stop recording after timeout
                if time.time() - start_time >= self.recording_timeout:
                    print("Recording timeout reached")
                    self.is_recording = False
        except Exception as e:
            print(f"Error in recording: {e}")
            self.is_recording = False

    def start_recording(self):
        """Start recording audio"""
        if not self.is_recording:
            self.is_recording = True
            self.thread = threading.Thread(target=self._record_audio)
            self.thread.daemon = True
            self.thread.start()

    def stop_recording(self):
        """Stop recording audio"""
        self.is_recording = False
        if self.thread:
            self.thread.join(timeout=1.0)  # Wait for thread to finish with timeout

    def get_text(self):
        """Get the latest recognized text if available"""
        try:
            return self.text_queue.get_nowait()
        except queue.Empty:
            return None

    def clear_queue(self):
        """Clear any pending text in the queue"""
        while not self.text_queue.empty():
            try:
                self.text_queue.get_nowait()
            except queue.Empty:
                break
