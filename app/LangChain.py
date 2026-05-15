# app/LangChain.py

import google.generativeai as genai
import os


def configurar_cadena_rag(vector_db=None):
    """
    Construye la cadena de respuesta.

    · vector_db=None  → modo IDENTIDAD: responde sólo con las
                        instrucciones del bot (saludos, quién eres…).
    · vector_db=<obj> → modo RAG: busca contexto en el vectorstore
                        y lo añade al prompt.
    """

    # ==========================
    # Leer identidad del bot
    # ==========================
    base_dir = os.path.dirname(__file__)
    ruta_identidad = os.path.join(base_dir, "identidad_bot.txt")

    try:
        with open(ruta_identidad, "r", encoding="utf-8") as f:
            instrucciones = f.read()
    except FileNotFoundError:
        instrucciones = "Eres un asistente útil y amable."

    # ==========================
    # Configurar API de Gemini
    # ==========================
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY no está configurada")

    genai.configure(api_key=api_key)

    # ==========================
    # Clase interna de la cadena
    # ==========================
    class CadenaRAG:

        def __init__(self, vector_db, instrucciones):
            self.vector_db = vector_db          # None si modo identidad
            self.instrucciones = instrucciones
            self.model = genai.GenerativeModel("gemini-1.5-flash")

        def run(self, pregunta: str) -> str:
            try:
                # ── Modo RAG: hay documento cargado ──────────────────
                if self.vector_db is not None:
                    docs = self.vector_db.similarity_search(pregunta, k=3)
                    contexto = "\n".join(d.page_content for d in docs)

                    prompt = f"""{self.instrucciones}

A continuación tienes fragmentos del documento que el usuario ha cargado.
Úsalos para responder con precisión. Si la respuesta no está en el documento,
indícalo amablemente.

Contexto del documento:
{contexto}

Pregunta del usuario:
{pregunta}

Respuesta:"""

                # ── Modo identidad: sin documento ─────────────────────
                else:
                    prompt = f"""{self.instrucciones}

El usuario aún no ha cargado ningún documento.
Responde de forma amable y ofrécele la posibilidad de subir un archivo
(PDF, TXT o DOCX) para que puedas ayudarle con preguntas específicas.

Pregunta del usuario:
{pregunta}

Respuesta:"""

                response = self.model.generate_content(prompt)
                return response.text if response else "No se pudo generar respuesta."

            except Exception as e:
                return f"Error al generar respuesta: {str(e)}"

        def invoke(self, inputs: dict) -> dict:
            query = inputs.get("query", "")
            return {"result": self.run(query)}

    return CadenaRAG(vector_db, instrucciones)