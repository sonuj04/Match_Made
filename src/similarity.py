from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def compute_similarity(resume_vec, jd_vec):
    score = cosine_similarity(
        resume_vec.reshape(1, -1),
        jd_vec.reshape(1, -1)
    )[0][0]

    return float(score)
