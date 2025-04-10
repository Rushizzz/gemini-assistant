from elevenlabs.client import ElevenLabs
from elevenlabs import stream

API_KEY = 'sk_975be26752920428fb898baba312260c9125dbcb923d4291'

client = ElevenLabs(
  api_key=API_KEY,
)

audio_stream = client.text_to_speech.convert_as_stream(
    text="This is a test",
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    model_id="eleven_multilingual_v2"
)

# option 1: play the streamed audio locally
stream(audio_stream)

# option 2: process the audio bytes manually
for chunk in audio_stream:
    if isinstance(chunk, bytes):
        print(chunk)
