import streamlit as st
from io import BytesIO
from pypdf import PdfReader

from modules.interview_module import evaluate_interview
from modules.claim_checker import check_claims
from modules.ai_resume_analysis import analyze_resume


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="CareerBridge",
    page_icon="🎯",
    layout="wide"
)


# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.stApp { background-color: #f5f7fb; }
[data-testid="stSidebar"] { background-color: #10213b; }
[data-testid="stSidebar"] * { color: white !important; }
.main-title {
    font-size: 38px;
    font-weight: 800;
    color: #173b70;
}
.subtitle { color: #64748b; font-size: 16px; }
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
    "interview_transcript": "",
    "claim_results": [],
    "ai_resume_result": None
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
    ["Dashboard", "Student Intake", "Resume Analysis",
     "Interview Feedback", "Mentor Review"]
)

st.sidebar.divider()
st.sidebar.info("Student Career Readiness Platform")


# ---------------- DASHBOARD ----------------
if page == "Dashboard":
    st.markdown('<div class="main-title">CareerBridge</div>',
                unsafe_allow_html=True)
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
    col1.metric("Resume Analysis",
                "Ready" if st.session_state.resume_text else "Pending")
    col2.metric("Interview Feedback",
                "Available" if st.session_state.interview_feedback else "Pending")
    col3.metric("Mentor Review",
                "Available" if st.session_state.mentor_comments else "Pending")

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
    st.write("Upload your resume, job description and project evidence.")

    student_name = st.text_input(
        "Student Name", value=st.session_state.student_name
    )
    resume_file = st.file_uploader(
        "Upload Resume (PDF or TXT)", type=["pdf", "txt"]
    )
    jd_text = st.text_area(
        "Job Description", value=st.session_state.jd_text, height=200
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
        if not student_name.strip():
            st.error("Please enter student name.")
        elif not resume_file and not st.session_state.resume_text:
            st.error("Please upload a resume.")
        elif not jd_text.strip():
            st.error("Please enter a Job Description.")
        else:
            try:
                extracted_text = st.session_state.resume_text

                if resume_file:
                    if resume_file.name.lower().endswith(".pdf"):
                        pdf = PdfReader(BytesIO(resume_file.getvalue()))
                        extracted_text = "\n".join(
                            page.extract_text() or "" for page in pdf.pages
                        )
                    else:
                        extracted_text = resume_file.getvalue().decode(
                            "utf-8", errors="ignore"
                        )

                if not extracted_text.strip():
                    st.error(
                        "Resume text could not be extracted. "
                        "Try a text-based PDF or TXT file."
                    )
                else:
                    st.session_state.student_name = student_name.strip()
                    st.session_state.resume_text = extracted_text
                    st.session_state.jd_text = jd_text.strip()

                    if project_images:
                        st.session_state.project_images = project_images
                    if audio:
                        st.session_state.audio = audio

                    # Clear old results when intake changes
                    st.session_state.claim_results = []
                    st.session_state.ai_resume_result = None
                    st.success("Student information saved successfully!")

            except Exception as e:
                st.error(f"Resume extraction failed: {e}")

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
        for index, image_file in enumerate(st.session_state.project_images):
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
    st.write("Compare resume skills with job description requirements.")

    if not st.session_state.resume_text:
        st.warning("Please upload your resume first using Student Intake.")
    else:
        skill_list = [
            "Python", "Java", "SQL", "Machine Learning", "Deep Learning",
            "HTML", "CSS", "JavaScript", "React", "Node.js", "Django",
            "Flask", "AWS", "Azure", "Git", "Power BI", "Excel",
            "Data Analysis", "NLP"
        ]

        resume_lower = st.session_state.resume_text.lower()
        jd_lower = st.session_state.jd_text.lower()

        resume_skills = [
            skill for skill in skill_list if skill.lower() in resume_lower
        ]
        jd_skills = [
            skill for skill in skill_list if skill.lower() in jd_lower
        ]
        matched_skills = [
            skill for skill in jd_skills if skill in resume_skills
        ]
        missing_skills = [
            skill for skill in jd_skills if skill not in resume_skills
        ]

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

        if jd_skills:
            match_percentage = round(
                len(matched_skills) / len(jd_skills) * 100
            )
            st.subheader("📊 Job Readiness Overview")
            st.metric("Keyword Skill Match", f"{match_percentage}%")
            st.progress(match_percentage / 100)
        else:
            st.info("No predefined skills detected in the Job Description.")

        st.caption(
            "Keyword matching only. A skill appearing in a resume "
            "does not prove expertise."
        )

        # Evidence-based claim review
        st.divider()
        st.subheader("🔎 Evidence-Based Claim Review")
        project_text = st.text_area(
            "Describe your project evidence",
            placeholder=(
                "Example: Built a Python ML model using pandas "
                "and scikit-learn..."
            ),
            height=150,
            key="project_evidence_text"
        )

        if st.button("Review Skill Claims"):
            if not project_text.strip():
                st.warning("Please describe your project evidence first.")
            else:
                try:
                    results = check_claims(
                        st.session_state.resume_text, project_text
                    )
                    st.session_state.claim_results = results
                except Exception as e:
                    st.error(f"Claim review failed: {e}")

        for result in st.session_state.claim_results:
            st.markdown(f"### {result.get('claim', 'Skill claim')}")
            status = result.get("status", "Not reviewed")
            if status == "Supported":
                st.success(status)
            elif status == "Weakly Supported":
                st.warning(status)
            else:
                st.error(status)
            st.write(result.get("explanation", ""))

        # Nexus AI resume analysis
        st.divider()
        st.subheader("🤖 AI Resume Analysis (Nexus)")
        if st.button("Analyze Resume with Nexus AI", type="primary"):
            if not st.session_state.resume_text:
                st.warning("Please upload a resume first.")
            elif not st.session_state.jd_text:
                st.warning("Please add a Job Description first.")
            else:
                with st.spinner("Nexus AI is analyzing your resume..."):
                    try:
                        result = analyze_resume(
                            st.session_state.resume_text,
                            st.session_state.jd_text
                        )
                        st.session_state.ai_resume_result = result
                        st.success("AI Analysis completed!")
                    except Exception as e:
                        st.error(f"AI Analysis failed: {e}")

        ai_result = st.session_state.ai_resume_result
        if ai_result:
            st.subheader("📊 AI Analysis Results")
            st.markdown("**Matched Skills**")
            st.write(ai_result.get("matched_skills", []))
            st.markdown("**Missing Skills**")
            st.write(ai_result.get("missing_skills", []))
            st.markdown("**Supported Claims**")
            st.write(ai_result.get("supported_claims", []))
            st.markdown("**Weakly Supported Claims**")
            st.write(ai_result.get("weakly_supported_claims", []))
            st.markdown("**Unsupported Claims**")
            st.write(ai_result.get("unsupported_claims", []))
            st.markdown("**Summary**")
            st.write(ai_result.get("summary", ""))


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
            try:
                feedback = evaluate_interview(transcript)
                if "error" in feedback:
                    st.error(feedback["error"])
                else:
                    st.session_state.interview_feedback = feedback
                    st.session_state.interview_transcript = transcript
                    st.success("Interview answer processed!")
            except Exception as e:
                st.error(f"Interview analysis failed: {e}")

    feedback = st.session_state.interview_feedback
    if feedback:
        st.divider()
        st.subheader("📊 Answer Overview")
        st.metric("Word Count", feedback.get("word_count", 0))
        st.caption(
            "Prototype feedback only. Actual AI evaluation "
            "will be integrated through Nexus AI."
        )

        st.subheader("📝 Evaluation Rubric")
        with st.expander("Answer Structure", expanded=True):
            st.write(feedback.get("structure", ""))
        with st.expander("Specificity"):
            st.write(feedback.get("specificity", ""))
        with st.expander("Job Relevance"):
            st.write(feedback.get("relevance", ""))
        with st.expander("Individual Contribution"):
            st.write(feedback.get("personal_role", ""))

        st.subheader("🚀 Improvement Plan")
        for item in feedback.get("improvement_plan", []):
            st.write("•", item)

        st.subheader("💡 Practice Questions")
        for index, question in enumerate(
            feedback.get("practice_questions", []), start=1
        ):
            st.write(f"{index}. {question}")


# ---------------- MENTOR REVIEW ----------------
elif page == "Mentor Review":
    st.title("👨‍🏫 Mentor Review Dashboard")
    st.caption("Review student progress, evidence, and interview readiness.")

    st.subheader("👤 Student Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric(
        "Resume", "Uploaded" if st.session_state.resume_text else "Missing"
    )
    col2.metric(
        "Job Description", "Added" if st.session_state.jd_text else "Missing"
    )
    col3.metric("Project Evidence", len(st.session_state.project_images))

    st.info(
        f"Student Name: {st.session_state.student_name or 'Not provided'}"
    )
    st.divider()

    st.subheader("📄 Evidence-Based Resume Review")
    if st.session_state.claim_results:
        for result in st.session_state.claim_results:
            st.markdown(f"**Claim:** {result.get('claim', 'Skill claim')}")
            status = result.get("status", "Not reviewed")
            if status == "Supported":
                st.success(status)
            elif status == "Weakly Supported":
                st.warning(status)
            else:
                st.error(status)
            st.write(result.get("explanation", ""))
            st.divider()
    else:
        st.warning("No skill claim review available yet.")

    st.subheader("🤖 Nexus AI Resume Analysis")
    if st.session_state.ai_resume_result:
        st.json(st.session_state.ai_resume_result)
    else:
        st.info("Nexus AI analysis has not been generated yet.")

    st.subheader("🎤 Interview Performance")
    transcript = st.session_state.interview_transcript
    if transcript:
        st.success("Interview transcript available")
        st.write(f"Transcript word count: {len(transcript.split())}")
    else:
        st.warning("No interview transcript available.")

    if st.session_state.interview_feedback:
        st.write("Interview Feedback:")
        st.json(st.session_state.interview_feedback)
    else:
        st.info("Interview feedback has not been generated.")

    st.divider()
    st.subheader("🖼️ Project Evidence")
    if st.session_state.project_images:
        for i, image in enumerate(st.session_state.project_images):
            st.image(image, caption=f"Project Evidence {i + 1}", width=300)
    else:
        st.info("No project screenshots uploaded.")

    st.divider()
    st.subheader("📝 Mentor Comments")
    mentor_comments = st.text_area(
        "Feedback for student",
        value=st.session_state.mentor_comments,
        placeholder="Write feedback, suggestions, and improvement areas..."
    )

    if st.button("Save Mentor Feedback", type="primary"):
        st.session_state.mentor_comments = mentor_comments
        st.success("Mentor feedback saved successfully!")

    st.caption(
        "This dashboard supports human review. It does not automatically "
        "determine a student's hiring eligibility."
    )
