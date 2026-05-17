# app/data/vectorstores/vectorstore.py
import os
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


class VectorStore:
    def __init__(self, base_dir=None):
        self.base_dir = base_dir or os.path.join(os.getcwd(), "data", "vectorstores")
        os.makedirs(self.base_dir, exist_ok=True)

    def guardar(self, textos, embeddings, nombre="documento"):
        """Guarda los textos vectorizados en un índice FAISS"""
        docs = [Document(page_content=t) for t in textos]
        db = FAISS.from_documents(docs, embeddings)
        ruta = os.path.join(self.base_dir, nombre)
        db.save_local(ruta)
        return db

    def cargar(self, embeddings, nombre="documento"):
        """Carga un índice FAISS existente"""
        ruta = os.path.join(self.base_dir, nombre)
        if not os.path.exists(ruta):
            raise FileNotFoundError(f"No existe almacén para '{nombre}'")
        return FAISS.load_local(ruta, embeddings, allow_dangerous_deserialization=True)
