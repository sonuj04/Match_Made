import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from src.preprocessing import clean_text
from src.embeddings import get_embedding
from src.skill_extractor import extract_skills
from src.ranking import rank_resumes
from src.explain import categorize_score, generate_explanation
from src.pdf_parser import extract_text_from_pdf

st.set_page_config(page_title="Resume Matcher", layout="wide")

st.title("Resume Matching System")

jd_input = st.text_area("Paste Job Description")

uploaded_files = st.file_uploader(
    "Upload Resume Files (.txt or .pdf)(add multiple peoples files for comparison)",
    accept_multiple_files=True,
    type=["txt", "pdf"]
)

if st.button("Match Candidates"):

    if not jd_input or not uploaded_files:
        st.warning("Please provide JD and upload resumes.")
        st.stop()

    jd_clean = clean_text(jd_input)
    jd_embedding = get_embedding(jd_clean)
    jd_skills = extract_skills(jd_input)

    resume_data = []

    for file in uploaded_files:

        if file.type == "application/pdf":
            file.seek(0)
            text = extract_text_from_pdf(file)
        else:
            text = file.read().decode("utf-8", errors="ignore")

        if not text.strip():
            continue

        cleaned = clean_text(text)
        embedding = get_embedding(cleaned)
        skills = extract_skills(text)

        resume_data.append({
            "name": file.name,
            "embedding": embedding,
            "skills": skills
        })

    ranked = rank_resumes(resume_data, jd_embedding, jd_skills)

    if not ranked:
        st.warning("No valid resumes processed.")
        st.stop()


    df = pd.DataFrame(ranked)


    st.subheader("Summary Metrics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Candidates", len(df))
    col2.metric("Top Score", round(df.iloc[0]["final_score"], 3))
    col3.metric("Average Score", round(df["final_score"].mean(), 3))

    st.markdown("---")

    st.subheader("Ranked Candidates")

    display_df = df[["name", "final_score", "semantic_score", "skill_score"]]
    st.dataframe(display_df)


    st.subheader("Candidate Score Comparison")

    fig, ax = plt.subplots()
    ax.bar(df["name"], df["final_score"])
    ax.set_ylabel("Final Score")
    ax.set_xticklabels(df["name"], rotation=45, ha="right")
    st.pyplot(fig)

    st.markdown("---")

    st.subheader("Candidate Breakdown")

    for candidate in ranked:

        explanation = generate_explanation(
            candidate["skills"],
            jd_skills
        )

        category = categorize_score(candidate["final_score"])

        with st.expander(candidate["name"]):

            st.write(f"Final Score: {round(candidate['final_score'], 3)}")
            st.write(f"Semantic Score: {round(candidate['semantic_score'], 3)}")
            st.write(f"Skill Overlap Score: {round(candidate['skill_score'], 3)}")
            st.write(f"Category: {category}")

            st.write("Matched Skills:", explanation["matched_skills"])
            st.write("Missing Skills:", explanation["missing_skills"])
