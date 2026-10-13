#To access the environment variables from .env file
import streamlit as st
from pypdf import PdfReader
from llm import ask_ai
import json

#To load the environment variables from .env file
from dotenv import load_dotenv

#To access tools to communicate with the Google Gemini API
from google import genai

#To load the API Key
load_dotenv()

#To Connect Gemini API Key to the application
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

#To declare the model to be used for the application
MODEL = "gemini-3.5-flash-lite"

#Define a function to send a prompt
def ask_ai(prompt):
    #To send the prompt to the model and get the response
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )
    #To return the response text
    return response.text


#Load the API Key
load_dotenv()

#Connect to Gemini
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

#Choose the model
MODEL = "gemini-3.5-flash-lite"

#Creating text response function
def ask_ai(prompt):
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )
    return response.text


#To create JSON response function
def ask_ai_json(prompt):
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config={
            "response_format": "application/json"
        }
    )
    return json.loads(response.text)
    