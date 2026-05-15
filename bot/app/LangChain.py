# app/LangChain.py

import os
from groq import Groq


def configurar_cadena_rag(vector_db=None):
    """
    Construye la cadena de respuesta con Groq (Llama).
    · vector_db=None  → modo IDENTIDAD
    · vector_db=<obj> → modo RAG
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
    # Configurar API de Groq
    # ==========================
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY no está configurada")

    cliente = Groq(api_key=api_key)

    # ==========================
    # Clase interna de la cadena
    # ==========================
    class CadenaRAG:

        def __init__(self, vector_db, instrucciones, cliente):
            self.vector_db = vector_db
            self.instrucciones = instrucciones
            self.cliente = cliente
            # Modelo gratuito recomendado:
            self.modelo = "llama-3.3-70b-versatile"
            # Alternativa si gastas muchas requests:
            # self.modelo = "llama-3.1-8b-instant"

        def run(self, pregunta: str) -> str:
            try:
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

                else:
                    prompt = f"""{self.instrucciones}

El usuario aún no ha cargado ningún documento.
Responde de forma amable y ofrécele la posibilidad de subir un archivo
(PDF, TXT o DOCX) para que puedas ayudarle con preguntas específicas.

Pregunta del usuario:
{pregunta}

Respuesta:"""

                response = self.cliente.chat.completions.create(
                    model=self.modelo,
                    messages=[
                        {"role": "system", "content": self.instrucciones},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=2048
                )

                return response.choices[0].message.content

            except Exception as e:
                return f"Error al generar respuesta: {str(e)}"

        def invoke(self, inputs: dict) -> dict:
            query = inputs.get("query", "")
            return {"result": self.run(query)}

    return CadenaRAG(vector_db, instrucciones, cliente)