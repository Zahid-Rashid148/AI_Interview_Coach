# Import Streamlit
import streamlit as st

# Import PDF Reader
from pypdf import PdfReader

# Import AI Functions
from llm import ask_ai
from coach import analyze_profile
from coach import generate_questions

# Application Title
st.title("AI Interview Coach")

# Function to Read PDF
def read_pdf(file):

    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or " "

    return text


# Upload Resume
Resume_file = st.file_uploader(
    "Upload your Resume",
    type=["pdf"]
)

# Paste Job Description
JD_file = st.text_area(
    "Paste the Job Description",
    height=200
)

# Read Resume
Resume_text = ""

if Resume_file:

    Resume_text = read_pdf(Resume_file)

    if Resume_text.strip() == "":
        st.error("The uploaded resume is empty or could not be read.")

    else:
        st.success("Resume uploaded successfully!")

        with st.expander("View Resume"):
            st.text(Resume_text)


# To analyze the Resume

if Resume_file and Resume_text.strip():

    # Display Buttons in One Row

    col1, col2 = st.columns(2)

    with col1:

        Resume_Button = st.button("Analyze Resume")

    with col2:

        Profile_Button = st.button("Analyze My Profile")

    # Analyze Resume

    if Resume_Button:

        with st.spinner("Analyzing Resume..."):

            prompt = f"""
You are an expert AI Interview Coach.

Analyze the following resume.

RESUME:

{Resume_text}

Provide:

1. A short summary of the candidate.

2. Key skills found in the resume.

3. Strengths.

4. Weaknesses.

5. Suitable Job Roles.

6. Areas for Improvement.

7. Interview Preparation Tips.
"""

            st.session_state.Resume_text = Resume_text
            st.session_state.Analysis = ask_ai(prompt)

    # Analyze My Profile

    if Profile_Button:

        if JD_file.strip() == "":

            st.warning("Please paste the Job Description first.")

        else:

            with st.spinner("Analyzing Profile..."):
                st.session_state.pop("Questions",None)
                st.session_state.Resume_text = Resume_text
                st.session_state.Job_Description = JD_file

                st.session_state.Profile = analyze_profile(
                    Resume_text,
                    JD_file
                )

    # Display Resume Analysis

    if "Analysis" in st.session_state:

        st.success("Resume Analysis Completed Successfully!")

        st.subheader("Resume Analysis")

        st.write(st.session_state.Analysis)

    # Display Profile Analysis

    if "Profile" in st.session_state:

        p = st.session_state.Profile

        st.success("Profile Analysis Completed Successfully!")

        st.header(f"Role : {p.get('Role', 'N/A')}")

        st.metric(
            "Match Score",
            f"{p.get('Match Score', 0)}%"
        )

        st.write(p.get("Summary", ""))

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Matching Skills")

            for skill in p.get("Matching Skills", []):

                st.success(skill)

        with col2:

            st.subheader("Missing Skills")

            for skill in p.get("Missing Skills", []):

                st.error(skill)

        with st.expander("View Full JSON Response"):

            st.json(p)

# *To Generate Interview Questions after Profile Analysis*

if "Profile" in st.session_state:

    st.divider()
    st.header("Interview Questions")

    # *Select the number of Questions*

    num = st.slider(
        "How many Questions?",
        3,
        10,
        5
    )

    # *Generate Questions Button*

    if st.button("Generate Questions"):

        # *Clear previous interview data*

        st.session_state.pop("Questions", None)
        st.session_state.pop("messages", None)
        st.session_state.pop("Answers", None)
        st.session_state.pop("Current_q", None)

        with st.spinner("Generating Questions..."):

            result = generate_questions(
                st.session_state.Profile,
                st.session_state.Resume_text,
                st.session_state.Job_Description,
                num
            )

            # *Store Questions*

            st.session_state.Questions = result.get(
                "Questions",
                []
            )

            # *Start Interview*

            if len(st.session_state.Questions) > 0:

                st.session_state.interview_started = True
                st.session_state.Current_q = 0
                st.session_state.Answers = []

                st.session_state.messages = [
                    {
                        "Role": "Assistant",
                        "Content": f"**Q1.** {st.session_state.Questions[0]['Question']}"
                    }
                ]

                st.rerun()

# Display Generated Questions

# if "Questions" in st.session_state:

#     st.subheader("Generated Interview Questions")

#     for i, q in enumerate(
#         st.session_state.Questions,
#         start=1
#     ):

#         st.markdown(f"**Q{i}.** {q.get('Question', '')}")

#         st.caption(
#             f"Type: {q.get('Type', '')} | Skill: {q.get('Skill', '')}"
#         )

#         st.divider()

# To start the Interview when the questions are generated

if "Questions" in st.session_state and st.session_state.get("interview_started", False):

    st.divider()
    st.header("Interview")

    Questions = st.session_state.Questions
    Current = st.session_state.Current_q
    Total = len(Questions)

    st.progress(
        Current / Total,
        text=f"Answered {Current} of {Total}"
    )

    # Display previous conversation

    for message in st.session_state.messages:
        with st.chat_message(message["Role"]):
            st.markdown(message["Content"])

    # Ask remaining questions

    if Current < Total:

        Answer = st.chat_input("Type your answer")

        if Answer:

            q = Questions[Current]

            # Store user's answer in chat

            st.session_state.messages.append({
                "Role": "User",
                "Content": Answer
            })

            # Save answer

            st.session_state.Answers.append({
                "Question": q.get("Question"),
                "Type": q.get("Type"),
                "Skill": q.get("Skill"),
                "Answer": Answer
            })

            # Move to next question

            st.session_state.Current_q += 1
            Next = st.session_state.Current_q

            if Next < Total:

                Next_Text = (
                    f"**Q{Next+1}.** "
                    f"{Questions[Next]['Question']}"
                )

            else:

                Next_Text = "That's the end of the interview. Thank you!"

            # Assistant asks next question

            st.session_state.messages.append({
                "Role": "Assistant",
                "Content": Next_Text
            })

            st.rerun()

    else:

        st.success("Interview Complete!")