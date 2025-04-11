from google import genai

API_KEY = 'AIzaSyAvTjUm8ZRA9Y7dfYFvY5R9MqDjdNzCZVE'

client = genai.Client(api_key=API_KEY)

def ask_gemini(query):
    modified_query = f'this is the query {query} strictly give response in just 2 to 3 line skip the instruction phase'
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=modified_query
    )
    print(response.text)
    return response.text
