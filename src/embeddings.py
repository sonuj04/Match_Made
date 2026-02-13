from sentence_transformers import SentenceTransformer
from src.config import EMBEDDING_MODEL

model = SentenceTransformer(EMBEDDING_MODEL)

def get_embedding(text: str):
    return model.encode(text, convert_to_numpy=True)
