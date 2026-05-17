# app/chatbot.py

from app.loaders import Loader
from app.embeddings import Embeddings
from app.data.vectorstores.vectorstore import VectorStore
from app.LangChain import configurar_cadena_rag
from langchain_text_splitters import RecursiveCharacterTextSplitter


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

        # ✅ La cadena de identidad se crea UNA sola vez al iniciar.
        # Recibe vector_db=None → responde sólo con identidad.
        self._cadena_identidad = configurar_cadena_rag(vector_db=None)

        # Cache de cadenas RAG por documento ya cargado
        self._cadenas_doc: dict = {}

    # --------------------------------------------------
    # Cargar documento y construir índice FAISS
    # --------------------------------------------------
    def cargar_documento(self, ruta: str, nombre: str = "documento"):
        texto = self.loader.cargar_archivo(ruta)
        chunks = self.splitter.split_text(texto)

        db = self.store.guardar(
            textos=chunks,
            embeddings=self.embedding(),
            nombre=nombre
        )

        # Guardar cadena RAG para este documento en el cache
        self._cadenas_doc[nombre] = configurar_cadena_rag(vector_db=db)
        return db

    # --------------------------------------------------
    # Responder una pregunta
    #
    # Lógica:
    #   · Si `nombre` es None o no se ha cargado ningún
    #     documento con ese nombre → usa sólo identidad.
    #   · Si hay un documento cargado con ese nombre      
    #     → usa RAG (contexto del doc) + identidad.
    # --------------------------------------------------
    def responder(self, pregunta: str, nombre: str | None = None) -> str:

        # 1. Intentar usar cadena RAG del documento en cache
        if nombre and nombre in self._cadenas_doc:
            cadena = self._cadenas_doc[nombre]
            return cadena.run(pregunta)

        # 2. Intentar cargar el vectorstore desde disco (si existe)
        if nombre:
            try:
                db = self.store.cargar(self.embedding(), nombre)
                cadena = configurar_cadena_rag(vector_db=db)
                self._cadenas_doc[nombre] = cadena   # guardar en cache
                return cadena.run(pregunta)
            except FileNotFoundError:
                pass   # el documento no existe → usa identidad

        # 3. Sin documento → respuesta sólo con identidad
        return self._cadena_identidad.run(pregunta)
