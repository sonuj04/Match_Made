from src.config import STRONG_MATCH_THRESHOLD, MODERATE_MATCH_THRESHOLD

def categorize_score(score: float):
    if score >= STRONG_MATCH_THRESHOLD:
        return "Strong Match"
    elif score >= MODERATE_MATCH_THRESHOLD:
        return "Moderate Match"
    return "Weak Match"


def generate_explanation(resume_skills, jd_skills):
    matched = list(set(resume_skills) & set(jd_skills))
    missing = list(set(jd_skills) - set(resume_skills))

    return {
        "matched_skills": matched,
        "missing_skills": missing
    }
