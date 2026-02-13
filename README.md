# Resume and job matching system

An AI-powered Resume Screening System that matches resumes to job descriptions using **semantic NLP embeddings + hybrid skill based scoring**, with an interactive dashboard.



## How It Works

### Text Processing
- Lemmatization
- Stopword removal
- Noise cleaning (spaCy)


### Semantic Embeddings
Resumes and job descriptions are converted into dense vector embeddings using:

`all-MiniLM-L6-v2` (Sentence Transformers)


### Hybrid Scoring

Final score combines:

Final Score =  
0.7 × Semantic Similarity (cosine between embeddings) + 0.3 × Skill Coverage Score (% of required job skills found in resume)



## Installation 

### Clone Repository

```bash
git clone <your-repo-link>
cd resume_matcher
```

### Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Run Application

```bash
streamlit run app.py
```
Open in browser: `http://localhost:8501`

## NOTE
This system is designed as a decision support tool, not an autonomous hiring authority.
Human oversight is required to ensure fairness and reduce bias.