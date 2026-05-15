# app/LangChain.py

import google.generativeai as genai
import os

def configurar_cadena_rag(vector_db):

    # ==========================
    # Ruta correcta identidad
    # ==========================
    base_dir = os.path.dirname(__file__)

    ruta_identidad = os.path.join(
        base_dir,
        "identidad_bot.txt"
    )

    try:
        with open(
            ruta_identidad,
            "r",
            encoding="utf-8"
        ) as archivo:

            instrucciones = archivo.read()

    except FileNotFoundError:

        instrucciones = (
            "Eres un asistente útil."
        )

    # ==========================
    # API KEY
    # ==========================
    api_key = os.getenv(
        "GOOGLE_API_KEY"
    )

    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY no configurada"
        )

    genai.configure(
        api_key=api_key
    )

    class CadenaRAG:

        def __init__(
            self,
            vector_db,
            instrucciones
        ):

            self.vector_db = vector_db
            self.instrucciones = instrucciones

            self.model = genai.GenerativeModel(
                "gemini-1.5-flash"
            )

        def run(self, pregunta):

            try:

                docs = self.vector_db.similarity_search(
                    pregunta,
                    k=3
                )

                contexto = "\n".join(
                    [
                        doc.page_content
                        for doc in docs
                    ]
                )

                prompt = f"""
{self.instrucciones}

Contexto:
{contexto}

Pregunta:
{pregunta}

Respuesta:
"""

                response = self.model.generate_content(
                    prompt
                )

                if response:
                    return response.text

                return "No se pudo generar respuesta"

            except Exception as e:

                return f"Error: {str(e)}"

        def invoke(self, inputs):

            query = inputs.get(
                "query",
                ""
            )

            return {
                "result": self.run(query)
            }

    return CadenaRAG(
        vector_db,
        instrucciones
    )