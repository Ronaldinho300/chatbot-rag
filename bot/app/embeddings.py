# Crear los embeddings (vectores numéricos) del texto.
# app/embeddings.py
from langchain_huggingface import HuggingFaceEmbeddings


class Embeddings:

    def __init__(self):
        self.modelo = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    def __call__(self):
        return self.modelo