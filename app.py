
import streamlit as st
from pypdf import PdfReader
from io import BytesIO

st.set_page_config(
    page_title="CareerBridge",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 CareerBridge")
st.subheader("Evidence-Based Interview Readiness")

st.write("Prepare for placements using evidence-based analysis.")

st.divider()

st.header("Student Intake")

student_name = st.text_input("Student Name")

resume = st.file_uploader(
    "Upload Resume",
    type=["pdf", "txt"]
)

job_description = st.text_area(
    "Paste Job Description",
    height=200
)

project_images = st.file_uploader(
    "Upload Project Screenshots",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

audio = st.audio_input(
    "Record: Tell me about a project you are proud of."
)

if st.button("Analyze My Readiness"):

    if not student_name.strip():
        st.warning("Please enter your name.")

    elif not resume:
        st.warning("Please upload your resume.")

    elif not job_description.strip():
        st.warning("Please enter job description.")

    elif not project_images:
        st.warning("Please upload project screenshots.")

    elif not audio:
        st.warning("Please record your interview answer.")

    else:
        st.success("All inputs received!")

        try:
            if resume.name.endswith(".pdf"):
                reader = PdfReader(BytesIO(resume.getvalue()))

                resume_text = ""

                for page in reader.pages:
                    resume_text += page.extract_text() or ""

            else:
                resume_text = resume.getvalue().decode("utf-8")

            st.subheader("📄 Extracted Resume Text")

            st.text_area(
                "Resume Content",
                resume_text,
                height=300
            )

            st.success("Resume text extraction successful!")

        except Exception as e:
            st.error(f"Resume extraction failed: {e}")
