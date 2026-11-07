
import streamlit as st
from pypdf import PdfReader
from io import BytesIO

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="CareerBridge",
    page_icon="🎯",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #f5f7fb;
}

[data-testid="stSidebar"] {
    background-color: #172554;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.main-title {
    font-size: 38px;
    font-weight: 800;
    color: #1e3a8a;
}

.subtitle {
    color: #64748b;
    font-size: 17px;
}

.section-title {
    color: #1e3a8a;
    font-size: 25px;
    font-weight: 700;
}

div.stButton > button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 22px;
}

div.stButton > button:hover {
    background-color: #1d4ed8;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

st.sidebar.markdown(
    "<h1>🎯 CareerBridge</h1>",
    unsafe_allow_html=True
)

st.sidebar.caption("Interview Readiness Platform")

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

st.sidebar.info(
    "Build credible portfolios "
    "and prepare for placements."
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "student_name" not in st.session_state:
    st.session_state.student_name = ""

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "jd_text" not in st.session_state:
    st.session_state.jd_text = ""

if "resume_skills" not in st.session_state:
    st.session_state.resume_skills = []

if "jd_skills" not in st.session_state:
    st.session_state.jd_skills = []

if "project_images" not in st.session_state:
    st.session_state.project_images = []

if "audio" not in st.session_state:
    st.session_state.audio = None

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🎯 CareerBridge</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Evidence-Based Interview Readiness'
    '</div>',
    unsafe_allow_html=True
)

st.divider()

# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if page == "Dashboard":

    st.header("Welcome to CareerBridge 👋")

    st.write(
        "Your AI-powered interview readiness workspace."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Resume Analysis", "Ready")

    with col2:
        st.metric("Interview Feedback", "Pending AI")

    with col3:
        st.metric("Mentor Review", "Available")

    st.divider()

    st.subheader("🚀 Getting Started")

    st.markdown("""
    1. Upload your resume.
    2. Add your job description.
    3. Upload project screenshots.
    4. Record your interview answer.
    5. Review your readiness results.
    """)

    st.info(
        "Resume analysis currently uses keyword matching. "
        "Nexus AI integration is planned."
    )

# --------------------------------------------------
# STUDENT INTAKE
# --------------------------------------------------

elif page == "Student Intake":

    st.header("📝 Student Intake")

    student_name = st.text_input(
        "Student Name",
        value=st.session_state.student_name
    )

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
            st.warning("Please enter student name.")

        elif not resume:
            st.warning("Please upload resume.")

        elif not jd.strip():
            st.warning("Please enter job description.")

        else:

            try:

                if resume.name.lower().endswith(".pdf"):

                    reader = PdfReader(
                        BytesIO(resume.getvalue())
                    )

                    text = ""

                    for p in reader.pages:
                        text += p.extract_text() or ""

                else:

                    text = resume.getvalue().decode(
                        "utf-8",
                        errors="replace"
                    )

                st.session_state.student_name = student_name
                st.session_state.resume_text = text
                st.session_state.jd_text = jd
                st.session_state.project_images = images
                st.session_state.audio = audio

                st.success("Resume and Job Description saved!")

                if text.strip():
                    st.success("Resume text extracted successfully!")
                else:
                    st.warning(
                        "No text found. PDF may be scanned."
                    )

            except Exception as e:

                st.error(f"Resume extraction failed: {e}")

    if st.session_state.resume_text:

        st.subheader("📄 Extracted Resume Preview")

        st.text_area(
            "Resume Content",
            st.session_state.resume_text,
            height=250
        )

# --------------------------------------------------
# RESUME ANALYSIS
# --------------------------------------------------

elif page == "Resume Analysis":

    st.header("📊 Resume Analysis")

    skills = [
        "Python",
        "Java",
        "SQL",
        "Machine Learning",
        "Deep Learning",
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Node.js",
        "Django",
        "Flask",
        "AWS",
        "Azure",
        "Git",
        "Power BI",
        "Excel",
        "Data Analysis",
        "NLP"
    ]

    resume_text = st.session_state.resume_text.lower()
    jd_text = st.session_state.jd_text.lower()

    if not resume_text or not jd_text:

        st.warning(
            "Please complete Student Intake first."
        )

    else:

        resume_skills = [
            s for s in skills
            if s.lower() in resume_text
        ]

        jd_skills = [
            s for s in skills
            if s.lower() in jd_text
        ]

        matched = [
            s for s in jd_skills
            if s in resume_skills
        ]

        missing = [
            s for s in jd_skills
            if s not in resume_skills
        ]

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Skills Found in Resume")

            if resume_skills:
                st.success(", ".join(resume_skills))
            else:
                st.info("No listed skills detected.")

        with col2:

            st.subheader("Skills in Job Description")

            if jd_skills:
                st.write(", ".join(jd_skills))
            else:
                st.info("No listed skills detected.")

        st.divider()

        st.subheader("✅ Matched Skills")

        if matched:
            st.success(", ".join(matched))
        else:
            st.warning("No matching skills detected.")

        st.subheader("📌 Potential Skill Gaps")

        if missing:
            st.warning(", ".join(missing))
        else:
            st.success("No keyword gaps detected.")

        st.caption(
            "Keyword matching only. A skill appearing "
            "in a resume does not prove expertise."
        )

# --------------------------------------------------
# INTERVIEW FEEDBACK
# --------------------------------------------------

elif page == "Interview Feedback":

    st.header("🎤 Interview Feedback")

    st.info(
        "Nexus AI interview analysis will be integrated here."
    )

    st.subheader("Planned Features")

    st.markdown("""
    - Audio transcription
    - Interview rubric scoring
    - Evidence-based feedback
    - Transcript quotations
    - Improvement plan
    - Five practice questions
    - Spoken feedback
    """)

    if st.session_state.audio:

        st.subheader("Recorded Interview Answer")

        st.audio(st.session_state.audio)

# --------------------------------------------------
# MENTOR REVIEW
# --------------------------------------------------

elif page == "Mentor Review":

    st.header("👩‍🏫 Mentor Review")

    st.info(
        "Mentor review workflow will be integrated here."
    )

    st.subheader("Student Information")

    st.write(
        "Student:",
        st.session_state.student_name or "Not provided"
    )

    st.subheader("Resume Status")

    if st.session_state.resume_text:

        st.success("Resume uploaded and extracted.")

    else:

        st.warning("Resume not available.")

    st.subheader("Mentor Comments")

    comments = st.text_area(
        "Enter mentor feedback",
        height=150
    )

    if st.button("Save Mentor Feedback"):

        if comments.strip():

            st.session_state.mentor_comments = comments

            st.success("Mentor feedback saved for this session.")

        else:

            st.warning("Please enter mentor comments.")
