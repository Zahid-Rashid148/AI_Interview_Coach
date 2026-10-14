import os
import json
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Create Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Select Gemini model
MODEL = "gemini-3.5-flash-lite"

# Function to get text response
def ask_ai(prompt):
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )
    return response.text

# Function to get JSON response
def ask_ai_json(prompt):
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )
    return json.loads(response.text)