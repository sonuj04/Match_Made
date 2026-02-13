import streamlit as st
import pandas as pd

from src.preprocessing import clean_text
from src.embeddings import get_embedding
from src.skill_extractor import extract_skills
from src.ranking import rank_resumes
from src.explain import categorize_score, generate_explanation

st.set_page_config(page_title="AI Resume Matcher", layout="wide")

st.title("📄 AI Resume Screening & Job Matching System")

st.markdown("Upload resumes and match them against a job description using semantic NLP.")

jd_input = st.text_area("Paste Job Description")

uploaded_files = st.file_uploader(
    "Upload Resume Files (.txt)",
    accept_multiple_files=True,
    type=["txt"]
)

if st.button("Match Candidates"):

    if jd_input and uploaded_files:

        jd_clean = clean_text(jd_input)
        jd_embedding = get_embedding(jd_clean)
        jd_skills = extract_skills(jd_input)

        resume_data = []

        for file in uploaded_files:
            text = file.read().decode("utf-8")

            cleaned = clean_text(text)
            embedding = get_embedding(cleaned)
            skills = extract_skills(text)

            resume_data.append({
                "name": file.name,
                "embedding": embedding,
                "skills": skills
            })

        ranked = rank_resumes(resume_data, jd_embedding)

        for candidate in ranked:
            explanation = generate_explanation(
                candidate["skills"],
                jd_skills
            )

            category = categorize_score(candidate["score"])

            st.subheader(candidate["name"])
            st.write(f"Score: {round(candidate['score'], 3)}")
            st.write(f"Category: {category}")

            st.write("Matched Skills:", explanation["matched_skills"])
            st.write("Missing Skills:", explanation["missing_skills"])
            st.markdown("---")

    else:
        st.warning("Please provide JD and upload resumes.")
