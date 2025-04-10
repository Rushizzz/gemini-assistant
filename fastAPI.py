from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8880/v1", api_key="not-needed"
)




def audio_out(data):
    with client.audio.speech.with_streaming_response.create(
        model="kokoro",
        voice="af_sky+af_bella", #single or multiple voicepack combo
        input=data
    ) as response:
        response.stream_to_file("output.mp3")
        from playsound3 import playsound
        playsound('output.mp3')

audio_out('hey hello this is Rushikesh')