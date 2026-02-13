import streamlit as st
import pandas as pd

from src.preprocessing import clean_text
from src.embeddings import get_embedding
from src.skill_extractor import extract_skills
from src.ranking import rank_resumes
from src.explain import categorize_score, generate_explanation
from src.pdf_parser import extract_text_from_pdf

st.set_page_config(page_title="AI Resume Matcher", layout="wide")

st.title("Job Matching System")

st.markdown("Upload resume and match them against a job description using semantic NLP.")

jd_input = st.text_area("Paste Job Description")

uploaded_files = st.file_uploader(
    "Upload Resume Files (.txt or .pdf)",
    accept_multiple_files=True,
    type=["txt", "pdf"]
)

if st.button("Match Candidates"):

    if jd_input and uploaded_files:

        jd_clean = clean_text(jd_input)
        jd_embedding = get_embedding(jd_clean)
        jd_skills = extract_skills(jd_input)

        resume_data = []


    for file in uploaded_files:

        if file.name.endswith(".pdf"):
            # Extract text using pdfplumber
            text = extract_text_from_pdf(file)

        elif file.name.endswith(".txt"):
            # Safe decode with fallback
            text = file.read().decode("utf-8", errors="ignore")

        else:
            st.warning(f"Unsupported file type: {file.name}")
            continue

        if not text or not text.strip():
            st.warning(f"Could not extract readable text from {file.name}")
            continue

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
