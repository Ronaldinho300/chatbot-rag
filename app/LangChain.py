import os

from groq import Groq


def configurar_cadena_rag(vector_db=None):
    """
    Construye la cadena de respuesta con Groq (Llama).
    - vector_db=None -> modo identidad
    - vector_db=<obj> -> modo RAG
    """

    possible_paths = [
        os.path.join(os.getcwd(), "data", "identidad_bot.txt"),
        os.path.join(os.path.dirname(__file__), "data", "identidad_bot.txt"),
        os.path.join(os.path.dirname(__file__), "identidad_bot.txt"),
    ]

    instrucciones = "Eres un asistente util y amable."
    for ruta_identidad in possible_paths:
        if os.path.exists(ruta_identidad):
            with open(ruta_identidad, "r", encoding="utf-8") as file:
                instrucciones = file.read()
            break

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY no esta configurada")

    cliente = Groq(api_key=api_key)

    class CadenaRAG:
        def __init__(self, vector_db, instrucciones, cliente):
            self.vector_db = vector_db
            self.instrucciones = instrucciones
            self.cliente = cliente
            self.modelo = "llama-3.3-70b-instant"

        def run(self, pregunta: str) -> str:
            try:
                if self.vector_db is not None:
                    docs = self.vector_db.similarity_search(pregunta, k=3)
                    contexto = "\n".join(doc.page_content for doc in docs)
                    prompt = f"""{self.instrucciones}

A continuacion tienes fragmentos del documento que el usuario ha cargado.
Usalos para responder con precision. Si la respuesta no esta en el documento,
indicalo amablemente.

Contexto del documento:
{contexto}

Pregunta del usuario:
{pregunta}

Respuesta:"""
                else:
                    prompt = f"""{self.instrucciones}

El usuario aun no ha cargado ningun documento.
Responde de forma amable y ofrecele la posibilidad de subir un archivo
(PDF, TXT o DOCX) para que puedas ayudarle con preguntas especificas.

Pregunta del usuario:
{pregunta}

Respuesta:"""

                response = self.cliente.chat.completions.create(
                    model=self.modelo,
                    messages=[
                        {"role": "system", "content": self.instrucciones},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.7,
                    max_tokens=2048,
                )

                return response.choices[0].message.content
            except Exception as exc:
                return f"Error al generar respuesta: {exc}"

        def invoke(self, inputs: dict) -> dict:
            query = inputs.get("query", "")
            return {"result": self.run(query)}

    return CadenaRAG(vector_db, instrucciones, cliente)
