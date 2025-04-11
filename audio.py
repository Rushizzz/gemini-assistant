from murf import Murf
import requests
from pydub import AudioSegment
from pydub.playback import play
import threading
import sounddevice as sd
import numpy as np
import queue

# Initialize the Murf client
client = Murf(api_key='ap2_89804798-2bd1-4016-a1fc-0181fa0e00c2')

# Create a queue for audio playback status
playback_status = queue.Queue()

def _play_audio(audio, callback=None):
    """Play audio in a separate thread"""
    try:
        # Convert to numpy array for playback
        samples = np.array(audio.get_array_of_samples())
        # Normalize the audio
        samples = samples / np.max(np.abs(samples))
        
        # Play the audio using sounddevice
        sd.play(samples, audio.frame_rate)
        sd.wait()  # Wait until audio is finished playing
        
        # Notify that playback is complete
        if callback:
            callback()
    except Exception as e:
        print(f"Error playing audio: {e}")
        if callback:
            callback()

def text_to_speech(data, callback=None):
    """Convert text to speech and play it in a separate thread"""
    try:
        # Generate the audio
        response = client.text_to_speech.generate(
            text=data,
            voice_id="en-UK-ruby",
            format="MP3",
            sample_rate=44100
        )

        # Download and save the audio file
        audio_url = response.audio_file
        audio_data = requests.get(audio_url).content

        with open("output.mp3", "wb") as file:
            file.write(audio_data)

        # Load the audio file
        audio = AudioSegment.from_mp3("output.mp3")
        
        # Play the audio in a separate thread
        audio_thread = threading.Thread(target=_play_audio, args=(audio, callback))
        audio_thread.daemon = True
        audio_thread.start()
        
    except Exception as e:
        print(f"Error in text-to-speech: {e}")
        if callback:
            callback()
    

