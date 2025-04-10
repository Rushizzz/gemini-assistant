from google import genai

API_KEY = 'AIzaSyAvTjUm8ZRA9Y7dfYFvY5R9MqDjdNzCZVE'

client = genai.Client(api_key=API_KEY)

query = 'whats todays weather in Mumbai'

response = client.models.generate_content(
    model="gemini-2.0-flash", contents=query
)
print(response.text)
