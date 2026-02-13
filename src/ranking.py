from src.similarity import compute_similarity
from src.config import SEMANTIC_WEIGHT, SKILL_WEIGHT

def compute_skill_overlap(resume_skills, jd_skills):
    if not jd_skills:
        return 0.0

    overlap = len(set(resume_skills) & set(jd_skills))
    return overlap / len(jd_skills)


def rank_resumes(resume_data, jd_vector, jd_skills):
    results = []

    for item in resume_data:
        semantic_score = compute_similarity(item["embedding"], jd_vector)
        skill_score = compute_skill_overlap(item["skills"], jd_skills)

        final_score = (
            SEMANTIC_WEIGHT * semantic_score +
            SKILL_WEIGHT * skill_score
        )

        results.append({
            "name": item["name"],
            "semantic_score": semantic_score,
            "skill_score": skill_score,
            "final_score": final_score,
            "skills": item["skills"]
        })

    results.sort(key=lambda x: x["final_score"], reverse=True)
    return results
