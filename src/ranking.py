from src.similarity import compute_similarity

def rank_resumes(resume_data, jd_vector):
    results = []

    for item in resume_data:
        score = compute_similarity(item["embedding"], jd_vector)

        results.append({
            "name": item["name"],
            "score": score,
            "skills": item["skills"]
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results
