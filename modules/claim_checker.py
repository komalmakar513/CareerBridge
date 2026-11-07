
def check_claims(resume_text, project_text=""):
    """
    Prototype evidence checker.
    Nexus AI will later perform actual semantic evidence verification.
    """

    claims = [
        "Python",
        "Java",
        "SQL",
        "Machine Learning",
        "Deep Learning",
        "React",
        "AWS",
        "Azure",
        "Data Analysis",
        "NLP"
    ]

    resume_text = resume_text.lower()
    project_text = project_text.lower()

    results = []

    for skill in claims:

        skill_lower = skill.lower()

        in_resume = skill_lower in resume_text
        in_project = skill_lower in project_text

        if in_resume and in_project:
            status = "Weakly Supported"
            explanation = (
                "Skill appears in resume and project description. "
                "Detailed evidence still requires verification."
            )

        elif in_resume:
            status = "Unsupported"
            explanation = (
                "Skill is mentioned in resume, but no project "
                "evidence was provided for this prototype."
            )

        elif in_project:
            status = "Weakly Supported"
            explanation = (
                "Skill appears in project information, "
                "but resume claim was not detected."
            )

        else:
            continue

        results.append({
            "claim": skill,
            "status": status,
            "explanation": explanation
        })

    return results
