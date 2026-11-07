
import streamlit as st
from pypdf import PdfReader
from io import BytesIO

st.set_page_config(
    page_title="CareerBridge",
    page_icon="🎯",
    layout="wide"
)

# Sidebar
st.sidebar.title("🎯 CareerBridge")
page = st.sidebar.radio(
    "Navigation",
    [
        "Student Intake",
        "Resume Analysis",
        "Interview Feedback",
        "Mentor Review"
    ]
)

st.title("🎯 CareerBridge")
st.caption("Evidence-Based Interview Readiness")

# Store results between pages
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "jd_text" not in st.session_state:
    st.session_state.jd_text = ""

if "resume_skills" not in st.session_state:
    st.session_state.resume_skills = []

if "jd_skills" not in st.session_state:
    st.session_state.jd_skills = []

if page == "Student Intake":

    st.header("📝 Student Intake")

    student_name = st.text_input("Student Name")

    resume = st.file_uploader(
        "Upload Resume",
        type=["pdf", "txt"]
    )

    jd = st.text_area(
        "Paste Job Description",
        height=200
    )

    images = st.file_uploader(
        "Upload Project Screenshots",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True
    )

    audio = st.audio_input(
        "Record: Tell me about a project you are proud of."
    )

    if st.button("Save & Extract Resume"):

        if not student_name.strip():
            st.warning("Enter student name.")

        elif not resume:
            st.warning("Upload resume.")

        elif not jd.strip():
            st.warning("Enter job description.")

        else:
            try:
                if resume.name.lower().endswith(".pdf"):
                    reader = PdfReader(BytesIO(resume.getvalue()))
                    text = ""

                    for p in reader.pages:
                        text += p.extract_text() or ""

                else:
                    text = resume.getvalue().decode("utf-8")

                st.session_state.resume_text = text
                st.session_state.jd_text = jd

                st.success("Resume and JD saved!")

            except Exception as e:
                st.error(str(e))

elif page == "Resume Analysis":

    st.header("📊 Resume Analysis")

    skills = [
        "Python", "Java", "SQL", "Machine Learning",
        "Deep Learning", "HTML", "CSS", "JavaScript",
        "React", "Node.js", "Django", "Flask",
        "AWS", "Azure", "Git", "Power BI",
        "Excel", "Data Analysis", "NLP"
    ]

    resume_text = st.session_state.resume_text.lower()
    jd_text = st.session_state.jd_text.lower()

    if not resume_text or not jd_text:
        st.info("First complete Student Intake.")
    else:
        resume_skills = [
            s for s in skills if s.lower() in resume_text
        ]

        jd_skills = [
            s for s in skills if s.lower() in jd_text
        ]

        matched = [s for s in jd_skills if s in resume_skills]
        missing = [s for s in jd_skills if s not in resume_skills]

        st.subheader("Skills Found in Resume")
        st.write(resume_skills)

        st.subheader("Matched Skills")
        st.success(matched if matched else "No matches")

        st.subheader("Potential Skill Gaps")
        st.warning(missing if missing else "No gaps detected")

        st.caption("Keyword matching only. Not AI verification.")

elif page == "Interview Feedback":

    st.header("🎤 Interview Feedback")
    st.info("Nexus AI transcription and rubric scoring will be integrated here.")
    st.write("Planned features:")
    st.write("- Interview transcript")
    st.write("- Transparent scoring rubric")
    st.write("- Evidence-based feedback")
    st.write("- Improvement plan")
    st.write("- Five practice questions")

elif page == "Mentor Review":

    st.header("👩‍🏫 Mentor Review")
    st.info("Mentor review panel will be integrated here.")
    st.write("Planned features:")
    st.write("- Review student evidence")
    st.write("- Review interview scores")
    st.write("- Approve or edit feedback")
    st.write("- Add mentor comments")
