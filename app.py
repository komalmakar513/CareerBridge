
import streamlit as st
from io import BytesIO
from pypdf import PdfReader

from modules.interview_module import evaluate_interview

from modules.claim_checker import check_claims


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="CareerBridge",
    page_icon="🎯",
    layout="wide"
)


# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.stApp {
    background-color: #f5f7fb;
}

[data-testid="stSidebar"] {
    background-color: #10213b;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.main-title {
    font-size: 38px;
    font-weight: 800;
    color: #173b70;
}

.subtitle {
    color: #64748b;
    font-size: 16px;
}

.stButton > button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 8px 18px;
}

.stButton > button:hover {
    background-color: #1d4ed8;
    color: white;
}

</style>
""", unsafe_allow_html=True)


# ---------------- SESSION STATE ----------------

defaults = {
    "student_name": "",
    "resume_text": "",
    "jd_text": "",
    "resume_skills": [],
    "jd_skills": [],
    "project_images": [],
    "audio": None,
    "mentor_comments": "",
    "interview_feedback": None,
    "interview_transcript": ""
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ---------------- SIDEBAR ----------------

st.sidebar.title("🎯 CareerBridge")
st.sidebar.caption("Evidence-Based Interview Readiness")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Student Intake",
        "Resume Analysis",
        "Interview Feedback",
        "Mentor Review"
    ]
)

st.sidebar.divider()
st.sidebar.info("Student Career Readiness Platform")


# ---------------- DASHBOARD ----------------

if page == "Dashboard":

    st.markdown(
        '<div class="main-title">CareerBridge</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Evidence-Based Interview Readiness</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.subheader("Welcome to CareerBridge 👋")

    st.write(
        "Prepare for placements with evidence-based resume analysis, "
        "interview practice and mentor feedback."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Resume Analysis",
            "Ready" if st.session_state.resume_text else "Pending"
        )

    with col2:
        st.metric(
            "Interview Feedback",
            "Available" if st.session_state.interview_feedback else "Pending"
        )

    with col3:
        st.metric(
            "Mentor Review",
            "Available" if st.session_state.mentor_comments else "Pending"
        )

    st.divider()

    st.subheader("🚀 Get Started")

    st.markdown("""
    - Upload your resume and job description.
    - Add project screenshots as supporting evidence.
    - Analyze your resume against job requirements.
    - Practice interview answers.
    - Review feedback with your placement mentor.
    """)

    st.info(
        "CareerBridge helps students identify skill gaps "
        "and improve interview readiness."
    )


# ---------------- STUDENT INTAKE ----------------

elif page == "Student Intake":

    st.title("📄 Student Intake")

    st.write(
        "Upload your resume, job description and project evidence."
    )

    student_name = st.text_input(
        "Student Name",
        value=st.session_state.student_name
    )

    resume_file = st.file_uploader(
        "Upload Resume (PDF or TXT)",
        type=["pdf", "txt"]
    )

    jd_text = st.text_area(
        "Job Description",
        value=st.session_state.jd_text,
        height=200
    )

    project_images = st.file_uploader(
        "Upload Project Screenshots",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True
    )

    audio = st.audio_input(
        "Record: Tell me about a project you are proud of"
    )

    if st.button("Save Student Information", type="primary"):

        st.session_state.student_name = student_name
        st.session_state.jd_text = jd_text

        if resume_file:

            try:

                if resume_file.name.lower().endswith(".pdf"):

                    pdf = PdfReader(
                        BytesIO(resume_file.getvalue())
                    )

                    resume_text = ""

                    for page_content in pdf.pages:
                        resume_text += (
                            page_content.extract_text() or ""
                        ) + "\n"

                else:

                    resume_text = resume_file.getvalue().decode(
                        "utf-8",
                        errors="ignore"
                    )

                st.session_state.resume_text = resume_text

            except Exception as e:

                st.error(f"Resume extraction failed: {e}")

        if project_images:

            st.session_state.project_images = project_images

        if audio:

            st.session_state.audio = audio

        st.success("Student information saved successfully!")

    if st.session_state.resume_text:

        st.subheader("Resume Preview")

        st.text_area(
            "Extracted Resume Text",
            st.session_state.resume_text,
            height=250,
            disabled=True
        )

    if st.session_state.project_images:

        st.subheader("Project Evidence")

        cols = st.columns(2)

        for index, image_file in enumerate(
            st.session_state.project_images
        ):

            with cols[index % 2]:

                st.image(
                    image_file.getvalue(),
                    caption=image_file.name,
                    width=350
                )

    if st.session_state.audio:

        st.subheader("Recorded Project Answer")

        st.audio(st.session_state.audio)


# ---------------- RESUME ANALYSIS ----------------

elif page == "Resume Analysis":

    st.title("📊 Resume Analysis")

    st.write(
        "Compare resume skills with job description requirements."
    )

    if not st.session_state.resume_text:

        st.warning(
            "Please upload your resume first using Student Intake."
        )

    else:

        skill_list = [
            "Python", "Java", "SQL",
            "Machine Learning", "Deep Learning",
            "HTML", "CSS", "JavaScript",
            "React", "Node.js",
            "Django", "Flask",
            "AWS", "Azure", "Git",
            "Power BI", "Excel",
            "Data Analysis", "NLP"
        ]

        resume_text = st.session_state.resume_text.lower()
        jd_text = st.session_state.jd_text.lower()

        resume_skills = [
            skill for skill in skill_list
            if skill.lower() in resume_text
        ]

        jd_skills = [
            skill for skill in skill_list
            if skill.lower() in jd_text
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

st.subheader("🔎 Evidence-Based Claim Review")

project_text = st.text_area(
    "Describe your project evidence",
    placeholder="Example: Built a Python ML model using pandas and scikit-learn...",
    height=150
)

if st.button("Review Skill Claims"):

    claim_results = check_claims(
        st.session_state.resume_text,
        project_text
    )

    st.session_state["claim_results"] = claim_results

claim_results = st.session_state.get("claim_results", [])

for result in claim_results:

    st.markdown(f"### {result['claim']}")

    if result["status"] == "Weakly Supported":
        st.warning(result["status"])

    else:
        st.error(result["status"])

    st.write(result["explanation"])

        st.subheader("Resume Skills")

        if resume_skills:

            st.write(", ".join(resume_skills))

        else:

            st.info("No predefined skills detected.")

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("✅ Matched Skills")

            if matched_skills:

                for skill in matched_skills:
                    st.write(f"• {skill}")

            else:

                st.write("No matching skills detected.")

        with col2:

            st.subheader("⚠️ Potential Skill Gaps")

            if missing_skills:

                for skill in missing_skills:
                    st.write(f"• {skill}")

            else:

                st.write("No potential gaps detected.")

        st.divider()

        st.caption(
            "This is keyword matching only. A skill appearing "
            "in a resume does not prove expertise."
        )


# ---------------- INTERVIEW FEEDBACK ----------------

elif page == "Interview Feedback":

    st.title("🎤 Interview Feedback")

    st.write(
        "Practice interview answers and receive structured "
        "improvement guidance."
    )

    transcript = st.text_area(
        "Enter your interview answer",
        value=st.session_state.interview_transcript,
        placeholder=(
            "Tell me about your project, your contribution, "
            "technologies used and challenges faced..."
        ),
        height=220
    )

    if st.button("Analyze Interview Answer", type="primary"):

        if not transcript.strip():

            st.warning("Please enter your interview answer first.")

        else:

            feedback = evaluate_interview(transcript)

            if "error" in feedback:

                st.error(feedback["error"])

            else:

                st.session_state.interview_feedback = feedback
                st.session_state.interview_transcript = transcript

                st.success("Interview answer processed!")

    feedback = st.session_state.interview_feedback

    if feedback:

        st.divider()

        st.subheader("📊 Answer Overview")

        st.metric(
            "Word Count",
            feedback["word_count"]
        )

        st.caption(
            "Prototype feedback only. Actual AI evaluation "
            "will be integrated through Nexus AI."
        )

        st.subheader("📝 Evaluation Rubric")

        with st.expander("Answer Structure", expanded=True):

            st.write(feedback["structure"])

        with st.expander("Specificity"):

            st.write(feedback["specificity"])

        with st.expander("Job Relevance"):

            st.write(feedback["relevance"])

        with st.expander("Individual Contribution"):

            st.write(feedback["personal_role"])

        st.subheader("🚀 Improvement Plan")

        for item in feedback["improvement_plan"]:

            st.write("•", item)

        st.subheader("💡 Practice Questions")

        for index, question in enumerate(
            feedback["practice_questions"],
            start=1
        ):

            st.write(f"{index}. {question}")


# ---------------- MENTOR REVIEW ----------------

elif page == "Mentor Review":

    st.title("👨‍🏫 Mentor Review")

    st.write(
        "Placement mentors can review student information "
        "and provide feedback."
    )

    st.subheader("Student Information")

    st.write(
        "**Student Name:**",
        st.session_state.student_name or "Not provided"
    )

    st.write(
        "**Resume Status:**",
        "Uploaded" if st.session_state.resume_text else "Not uploaded"
    )

    st.write(
        "**Project Evidence:**",
        len(st.session_state.project_images),
        "image(s)"
    )

    st.write(
        "**Interview Feedback:**",
        "Available" if st.session_state.interview_feedback else "Pending"
    )

    st.divider()

    mentor_comments = st.text_area(
        "Mentor Comments",
        value=st.session_state.mentor_comments,
        height=200,
        placeholder="Write suggestions for the student..."
    )

    if st.button("Save Mentor Feedback", type="primary"):

        st.session_state.mentor_comments = mentor_comments

        st.success("Mentor feedback saved successfully!")

    if st.session_state.mentor_comments:

        st.subheader("Saved Mentor Feedback")

        st.info(st.session_state.mentor_comments)
