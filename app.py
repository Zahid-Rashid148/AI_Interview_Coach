# #import streamlit as st

# #To Display Application Title
# #st.title("AI_Interview_Coach")

# #To Write a Message
# #st.write("Setup is Working. Let's get started!")

import streamlit as st
from pypdf import PdfReader
from llm import ask_ai
import os
import json
from dotenv import load_dotenv
from google import genai
# #Next Application Title
# st.title("AI_Interview_Coach")

# #To define PDF reading function
# #To extract text from all the pages
# def read_pdf(file):

#     Reader = PdfReader(file)

#     text = ""

#     for page in Reader.pages:

#         text += page.extract_text() or " "

#     return text


# #To allow User's to upload Resume
# Resume_file = st.file_uploader("Upload your Resume", type=["pdf"])


# #To allow User's to paste the Job Description
# JD_file = st.text_area("Paste the Job Description", height=200)


# #To process the uploaded Resume
# if Resume_file:

#     #To read the Resume
#     Resume_text = read_pdf(Resume_file)

#     #To check whether Resume is empty
#     if Resume_text.strip() == "":

#         st.error("The uploaded resume is empty or could not be read. Please upload a valid PDF file.")

#     else:

#         #To display success message
#         st.success("Resume uploaded and read successfully!")

#         #To display extracted Resume text
#         with st.expander("View Extracted Resume Text"):

#             st.text(Resume_text)


# #To analyze the Resume with Job Description
# if Resume_file and JD_file:

#     #To display Analyze Resume button
#     if st.button("Analyze Resume"):

#         #To prepare prompt for Gemini AI
#         prompt = f"""
# You are an expert AI Interview Coach.

# Analyze the candidate's resume against the given job description.

# RESUME:

# {Resume_text}

# JOB DESCRIPTION:

# {JD_file}

# Provide the following:

# 1. A short summary of the candidate.

# 2. Key skills found in the resume.

# 3. Skills required by the job description.

# 4. Matching skills.

# 5. Missing skills.

# 6. Overall suitability for the role.

# 7. Areas the candidate should prepare for the job.
# """

#         #To display loading spinner
#         with st.spinner("Analyzing Resume..."):

#             #To send prompt to Gemini
#             Analysis = ask_ai(prompt)

#         #To display success message
#         st.success("Analysis Completed Successfully!")

#         #To display analysis heading
#         st.subheader("Resume Analysis")

#         #To display AI generated analysis
#         st.write(Analysis)


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
    
