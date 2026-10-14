# Import the JSON response function from llm.py

from llm import ask_ai_json


# Function to analyze the candidate's profile

def analyze_profile(resume_text, job_description):

    # Create the prompt for Gemini AI

    prompt = f"""
You are an expert technical recruiter.

Compare the candidate's resume with the job description.

Resume:

{resume_text}

Job Description:

{job_description}

Return ONLY valid JSON with exactly these keys:

{{
    "Candidate's Name": "",
    "Role": "",
    "Matching Skills": [],
    "Missing Skills": [],
    "Match Score": 0,
    "Summary": ""
}}

Rules:

1. Use only information available in the resume.
2. Do not invent skills.
3. Match Score should be between 0 and 100.
4. Return only valid JSON.
"""

    # Get the JSON response from Gemini

    analysis = ask_ai_json(prompt)

    # Return the analysis

    return analysis


# Function to generate interview questions

def generate_questions(analysis, resume_text, job_description, num_questions=5):

    # Create the prompt for Gemini AI

    prompt = f"""
You are an experienced interviewer hiring for the role of {analysis.get('Role', 'this job')}.

Generate exactly {num_questions} interview questions for this candidate.

Use this mix:

- Technical questions based on the candidate's matching skills.
- At least one question about a project mentioned in the resume.
- At least one question about a missing skill.
- One behavioral question about teamwork, communication, challenges, or deadlines.

Candidate Resume:

{resume_text}

Job Description:

{job_description}

Matching Skills:

{analysis.get("Matching Skills", [])}

Missing Skills:

{analysis.get("Missing Skills", [])}

Return ONLY valid JSON in this format:

{{
    "Questions": [
        {{
            "Question": "...",
            "Type": "Technical",
            "Skill": "Python"
        }},
        {{
            "Question": "...",
            "Type": "Behavioral",
            "Skill": "Communication"
        }}
    ]
}}
"""

    # Get the JSON response from Gemini

    questions = ask_ai_json(prompt)

    # Return the generated questions

    return questions