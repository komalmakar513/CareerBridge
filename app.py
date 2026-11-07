
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
st.write("Prepare for placements with evidence-based analysis.")

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
        try:
            # Extract resume text
            if resume.name.lower().endswith(".pdf"):
                reader = PdfReader(BytesIO(resume.getvalue()))
                resume_text = ""

                for page in reader.pages:
                    resume_text += page.extract_text() or ""

            else:
                resume_text = resume.getvalue().decode("utf-8")

            st.success("Resume extracted successfully!")

            st.subheader("📄 Resume Content")
            st.text_area(
                "Extracted Resume Text",
                resume_text,
                height=250
            )

            # Basic skill matching
            skills = [
                "Python", "Java", "SQL", "Machine Learning",
                "Deep Learning", "HTML", "CSS", "JavaScript",
                "React", "Node.js", "Django", "Flask",
                "AWS", "Azure", "Git", "Power BI",
                "Excel", "Data Analysis", "NLP"
            ]

            resume_lower = resume_text.lower()
            jd_lower = job_description.lower()

            resume_skills = [
                skill for skill in skills
                if skill.lower() in resume_lower
            ]

            jd_skills = [
                skill for skill in skills
                if skill.lower() in jd_lower
            ]

            matched_skills = [
                skill for skill in jd_skills
                if skill in resume_skills
            ]

            missing_skills = [
                skill for skill in jd_skills
                if skill not in resume_skills
            ]

            st.divider()
            st.header("📊 Resume & Job Description Analysis")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Skills Found in Resume")
                if resume_skills:
                    st.write(", ".join(resume_skills))
                else:
                    st.info("No listed skills detected.")

            with col2:
                st.subheader("Skills Mentioned in Job")
                if jd_skills:
                    st.write(", ".join(jd_skills))
                else:
                    st.info("No listed skills detected.")

            st.subheader("✅ Matched Skills")
            if matched_skills:
                st.success(", ".join(matched_skills))
            else:
                st.warning("No matching skills detected.")

            st.subheader("📌 Potential Skill Gaps")
            if missing_skills:
                st.warning(", ".join(missing_skills))
            else:
                st.success("All detected JD skills appear in resume.")

            st.caption(
                "This is basic keyword matching, not AI verification. "
                "A skill appearing in a resume does not prove expertise."
            )

        except Exception as e:
            st.error(f"Analysis failed: {e}")
