
def evaluate_interview(transcript):
    """
    Prototype feedback.
    Real AI evaluation will be connected through Nexus AI.
    """

    transcript = transcript.strip()

    if not transcript:
        return {
            "error": "Please enter your interview answer."
        }

    word_count = len(transcript.split())

    return {
        "word_count": word_count,
        "structure": "Review whether your answer has a clear beginning, middle and end.",
        "specificity": "Include concrete examples, technologies and measurable results.",
        "relevance": "Connect your answer to the job description.",
        "personal_role": "Clearly explain your individual contribution.",
        "improvement_plan": [
            "Start with the problem your project solved.",
            "Explain your individual contribution.",
            "Describe the technologies you used.",
            "Explain one challenge and how you solved it.",
            "Mention the outcome and what you learned."
        ],
        "practice_questions": [
            "What problem did your project solve?",
            "What was your individual contribution?",
            "Why did you choose these technologies?",
            "What was your biggest technical challenge?",
            "How would you improve your project?"
        ]
    }
