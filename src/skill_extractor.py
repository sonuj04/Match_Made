from src.config import SKILLS

def extract_skills(text: str):
    text = text.lower()
    found = [skill for skill in SKILLS if skill in text]
    return list(set(found))
