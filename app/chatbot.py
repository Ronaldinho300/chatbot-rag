# app/chatbot.py
from loaders import Loader
from embeddings import Embeddings
from data.vectorstores.vectorstore import VectorStore
from LangChain import configurar_cadena_rag
from langchain.text_splitter import RecursiveCharacterTextSplitter  # añadido para chunking

class Chatbot:
    def __init__(self):
        self.loader = Loader()
        self.embedding = Embeddings()
        self.store = VectorStore()
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )

    def cargar_documento(self, ruta, nombre="documento"):
        texto = self.loader.cargar_archivo(ruta)
        # Dividir en fragmentos pequeños
        chunks = self.splitter.split_text(texto)
        db = self.store.guardar(
            textos=chunks,
            embeddings=self.embedding(),   # ← ¡llamada a __call__!
            nombre=nombre
        )
        return db

    def responder(self, pregunta, nombre="documento"):
        vector_db = self.store.cargar(
            self.embedding(),   # ← ¡llamada a __call__!
            nombre
        )
        chain = configurar_cadena_rag(vector_db)
        respuesta = chain.run(pregunta)
        return respuesta